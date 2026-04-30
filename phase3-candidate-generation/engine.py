from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re

import pandas as pd


@dataclass(frozen=True)
class Preferences:
    location: str
    budget: str
    cuisine_tokens: list[str]
    minimum_rating: float
    additional_tags: list[str]


@dataclass(frozen=True)
class RunSummary:
    input_rows: int
    output_rows: int
    fallback_stage: str
    filters_applied: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def _tokenize(text: str) -> set[str]:
    if not text:
        return set()
    return {token.strip().lower() for token in re.split(r"[,/|]", text) if token.strip()}


def _normalize_budget(value: str) -> str:
    aliases = {
        "low": "low",
        "budget": "low",
        "cheap": "low",
        "medium": "medium",
        "mid": "medium",
        "moderate": "medium",
        "high": "high",
        "premium": "high",
        "expensive": "high",
    }
    key = (value or "").strip().lower()
    if key not in aliases:
        raise ValueError("Budget must be one of: low, medium, high (or known synonyms).")
    return aliases[key]


def parse_preferences(payload: dict) -> Preferences:
    location = str(payload.get("location", "")).strip().lower()
    if not location:
        raise ValueError("location is required.")

    budget = _normalize_budget(str(payload.get("budget", "")))

    cuisine_tokens = payload.get("cuisine_tokens")
    if isinstance(cuisine_tokens, list):
        cuisines = sorted({str(c).strip().lower() for c in cuisine_tokens if str(c).strip()})
    else:
        cuisine_text = str(payload.get("cuisine", ""))
        cuisines = sorted(_tokenize(cuisine_text))
    if not cuisines:
        raise ValueError("At least one cuisine is required.")

    try:
        minimum_rating = float(payload.get("minimum_rating", 0))
    except ValueError as exc:
        raise ValueError("minimum_rating must be numeric.") from exc
    if minimum_rating < 0 or minimum_rating > 5:
        raise ValueError("minimum_rating must be in range 0..5.")

    additional = payload.get("additional_tags", [])
    if isinstance(additional, list):
        additional_tags = sorted({str(t).strip().lower() for t in additional if str(t).strip()})
    else:
        additional_tags = sorted(_tokenize(str(payload.get("additional_preferences", ""))))

    return Preferences(
        location=location,
        budget=budget,
        cuisine_tokens=cuisines,
        minimum_rating=round(minimum_rating, 2),
        additional_tags=additional_tags,
    )


def load_dataset(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")
    frame = pd.read_csv(csv_path)
    required = {"name", "location", "cuisines", "estimated_cost_for_two", "rating"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {sorted(missing)}")
    return frame


def _budget_match(cost: float | None, budget: str) -> bool:
    if pd.isna(cost):
        return True
    if budget == "low":
        return cost <= 500
    if budget == "medium":
        return 500 < cost <= 1200
    return cost > 1200


def _location_match(restaurant_location: str, pref_location: str) -> bool:
    left = str(restaurant_location).strip().lower()
    right = pref_location.strip().lower()
    return right in left or left in right


def _cuisine_overlap(cuisine_text: str, requested: list[str]) -> int:
    tokens = _tokenize(str(cuisine_text))
    return len(tokens.intersection(set(requested)))


def _score_row(row: pd.Series, pref: Preferences) -> float:
    overlap = _cuisine_overlap(str(row["cuisines"]), pref.cuisine_tokens)
    rating_score = float(row["rating"]) if not pd.isna(row["rating"]) else 0.0
    budget_score = 1.0 if _budget_match(row["estimated_cost_for_two"], pref.budget) else 0.0
    return round(overlap * 2 + rating_score + budget_score, 3)


def _apply_constraints(
    frame: pd.DataFrame,
    pref: Preferences,
    *,
    use_location: bool,
    use_budget: bool,
    use_rating: bool,
    use_cuisine: bool,
) -> pd.DataFrame:
    df = frame.copy()

    if use_location:
        df = df[df["location"].map(lambda x: _location_match(str(x), pref.location))]
    if df.empty:
        return df
        
    if use_budget:
        df = df[df["estimated_cost_for_two"].map(lambda x: _budget_match(x, pref.budget))]
    if df.empty:
        return df
        
    if use_rating:
        df = df[df["rating"].isna() | (df["rating"] >= pref.minimum_rating)]
    if df.empty:
        return df
        
    if use_cuisine:
        df = df[df["cuisines"].map(lambda x: _cuisine_overlap(str(x), pref.cuisine_tokens) > 0)]

    return df


def generate_candidates(frame: pd.DataFrame, pref: Preferences, top_n: int = 30) -> tuple[pd.DataFrame, RunSummary]:
    stages = [
        ("strict", dict(use_location=True, use_budget=True, use_rating=True, use_cuisine=True)),
        ("relax_budget", dict(use_location=True, use_budget=False, use_rating=True, use_cuisine=True)),
        ("relax_rating_budget", dict(use_location=True, use_budget=False, use_rating=False, use_cuisine=True)),
        ("relax_cuisine_rating_budget", dict(use_location=True, use_budget=False, use_rating=False, use_cuisine=False)),
        ("global_fallback", dict(use_location=False, use_budget=False, use_rating=False, use_cuisine=False)),
    ]

    selected = frame.iloc[0:0].copy()
    stage_name = "strict"
    applied: dict[str, bool] = {}
    for stage_name, constraints in stages:
        attempt = _apply_constraints(frame, pref, **constraints)
        if len(attempt) > 0:
            selected = attempt
            applied = constraints
            break

    selected = selected.copy()
    selected["candidate_score"] = selected.apply(lambda row: _score_row(row, pref), axis=1)
    selected["cuisine_overlap"] = selected["cuisines"].map(lambda x: _cuisine_overlap(str(x), pref.cuisine_tokens))
    selected = selected.sort_values(by=["candidate_score", "cuisine_overlap", "rating"], ascending=[False, False, False])
    selected = selected.head(top_n).reset_index(drop=True)

    summary = RunSummary(
        input_rows=len(frame),
        output_rows=len(selected),
        fallback_stage=stage_name,
        filters_applied=[key for key, value in applied.items() if value],
    )
    return selected, summary


def save_outputs(candidates: pd.DataFrame, summary: RunSummary, output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "candidates.csv"
    json_path = output_dir / "candidates.json"
    summary_path = output_dir / "last_run_summary.json"

    candidates.to_csv(csv_path, index=False)
    json_path.write_text(candidates.to_json(orient="records", indent=2), encoding="utf-8")
    summary_path.write_text(json.dumps(summary.to_dict(), indent=2), encoding="utf-8")

    return {
        "candidates_csv": str(csv_path),
        "candidates_json": str(json_path),
        "summary_json": str(summary_path),
    }

