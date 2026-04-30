from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

from datasets import load_dataset
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_CSV = OUTPUT_DIR / "restaurants_cleaned.csv"
QUALITY_REPORT = OUTPUT_DIR / "quality_report.json"
PREFERENCES_FILE = OUTPUT_DIR / "last_preferences.json"


def _parse_cost(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip().lower()
    if not text:
        return None
    numbers = re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))
    if not numbers:
        return None
    parsed = [float(n) for n in numbers]
    return sum(parsed) / len(parsed)


def _normalize_location(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    aliases = {
        "bengaluru": "bangalore",
        "banglore": "bangalore",
        "bombay": "mumbai",
        "delhi ncr": "delhi",
    }
    normalized = str(value).strip().lower()
    if not normalized:
        return None
    return aliases.get(normalized, normalized)


def _normalize_cuisines(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    raw = str(value).strip()
    if not raw:
        return None
    tokens = [part.strip().lower() for part in re.split(r"[,/|]", raw) if part.strip()]
    tokens = sorted(set(tokens))
    return ", ".join(tokens) if tokens else None


def _clamp_rating(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    
    text = str(value).strip().lower()
    if "/" in text:
        text = text.split("/")[0].strip()
    
    try:
        numeric = float(text)
    except (TypeError, ValueError):
        return None
        
    if numeric < 0 or numeric > 5:
        return None
    return round(numeric, 2)


def _standardize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    specs: dict[str, tuple[str, ...]] = {
        "name": ("restaurant_name", "res_name", "name"),
        "location": ("city", "location", "locality"),
        "cuisines": ("cuisine", "cuisines", "food_type"),
        "average_cost_for_two": ("average_cost_for_two", "cost_for_two", "price_for_two", "approx_cost(for two people)"),
        "aggregate_rating": ("aggregate_rating", "rating", "user_rating", "rate"),
    }

    lower_map = {column.lower().strip(): column for column in frame.columns}
    rename_map: dict[str, str] = {}
    for canonical, aliases in specs.items():
        for alias in aliases:
            source = lower_map.get(alias.lower())
            if source:
                rename_map[source] = canonical
                break

    standardized = frame.rename(columns=rename_map).copy()
    for required in specs:
        if required not in standardized.columns:
            standardized[required] = pd.NA
    return standardized


def _quality_report(df: pd.DataFrame) -> dict[str, int | bool]:
    dedupe_key = (
        df["name"].fillna("").str.lower().str.strip()
        + "|"
        + df["location"].fillna("").str.lower().str.strip()
        + "|"
        + df["cuisines"].fillna("").str.lower().str.strip()
    )
    report = {
        "row_count": len(df),
        "missing_name_count": int(df["name"].isna().sum()),
        "missing_location_count": int(df["location"].isna().sum()),
        "missing_cuisine_count": int(df["cuisines"].isna().sum()),
        "missing_cost_count": int(df["estimated_cost_for_two"].isna().sum()),
        "missing_rating_count": int(df["rating"].isna().sum()),
        "duplicate_key_count": int(dedupe_key.duplicated().sum()),
        "invalid_rating_count": int(((df["rating"] < 0) | (df["rating"] > 5)).fillna(False).sum()),
    }
    report["quality_gate_passed"] = (
        report["missing_name_count"] == 0
        and report["missing_location_count"] == 0
        and report["invalid_rating_count"] == 0
    )
    return report


def run_pipeline() -> dict[str, str | int | bool]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
    frame = _standardize_columns(dataset.to_pandas())

    frame["name"] = frame["name"].astype(str).str.strip()
    frame["location"] = frame["location"].map(_normalize_location)
    frame["cuisines"] = frame["cuisines"].map(_normalize_cuisines)
    frame["estimated_cost_for_two"] = frame["average_cost_for_two"].map(_parse_cost)
    frame["rating"] = frame["aggregate_rating"].map(_clamp_rating)

    frame = frame.dropna(subset=["name", "location"])
    frame = frame[frame["name"].str.len() > 0]

    curated = frame[["name", "location", "cuisines", "estimated_cost_for_two", "rating"]].copy()
    dedupe_key = (
        curated["name"].str.lower().str.strip()
        + "|"
        + curated["location"].fillna("").str.lower().str.strip()
        + "|"
        + curated["cuisines"].fillna("").str.lower().str.strip()
    )
    curated = curated.loc[~dedupe_key.duplicated()].reset_index(drop=True)

    report = _quality_report(curated)
    curated.to_csv(OUTPUT_CSV, index=False)
    QUALITY_REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    return {
        "output_csv": str(OUTPUT_CSV),
        "quality_report": str(QUALITY_REPORT),
        "rows_written": len(curated),
        "quality_gate_passed": bool(report["quality_gate_passed"]),
    }


def save_preferences(preferences: dict[str, str]) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PREFERENCES_FILE.write_text(json.dumps(preferences, indent=2), encoding="utf-8")
    return str(PREFERENCES_FILE)


if __name__ == "__main__":
    print("Running pipeline...")
    result = run_pipeline()
    print(f"Pipeline finished: {json.dumps(result, indent=2)}")

