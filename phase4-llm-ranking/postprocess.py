from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class RankedItem:
    rank: int
    restaurant_name: str
    fit_score: float
    explanation: str


@dataclass(frozen=True)
class RankedResult:
    summary: str
    recommendations: list[RankedItem]

    def to_dict(self) -> dict:
        return asdict(self)


def _parse_json_response(raw_text: str) -> dict:
    stripped = raw_text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.startswith("json"):
            stripped = stripped[4:].strip()
    return json.loads(stripped)


def parse_ranked_result(raw_text: str) -> RankedResult:
    payload = _parse_json_response(raw_text)
    summary = str(payload.get("summary", "")).strip()
    rows = payload.get("recommendations", [])
    if not isinstance(rows, list):
        raise ValueError("recommendations must be a list.")

    recommendations: list[RankedItem] = []
    for row in rows:
        rank = int(row["rank"])
        name = str(row["restaurant_name"]).strip()
        fit_score = float(row["fit_score"])
        explanation = str(row["explanation"]).strip()
        recommendations.append(
            RankedItem(
                rank=rank,
                restaurant_name=name,
                fit_score=max(0.0, min(10.0, fit_score)),
                explanation=explanation,
            )
        )

    recommendations = sorted(recommendations, key=lambda r: r.rank)
    return RankedResult(summary=summary, recommendations=recommendations)


def validate_against_candidates(result: RankedResult, candidates: list[dict], top_k: int) -> RankedResult:
    allowed_names = {str(row.get("name", "")).strip().lower() for row in candidates}
    filtered: list[RankedItem] = []
    seen: set[str] = set()

    for item in result.recommendations:
        key = item.restaurant_name.strip().lower()
        if key not in allowed_names:
            continue
        if key in seen:
            continue
        seen.add(key)
        filtered.append(item)
        if len(filtered) >= top_k:
            break

    # If model returns fewer valid rows, backfill deterministically from candidates.
    if len(filtered) < top_k:
        rank_seed = len(filtered) + 1
        for row in candidates:
            name = str(row.get("name", "")).strip()
            key = name.lower()
            if not name or key in seen:
                continue
            filtered.append(
                RankedItem(
                    rank=rank_seed,
                    restaurant_name=name,
                    fit_score=5.0,
                    explanation="Fallback selection from candidate list due to insufficient validated LLM output.",
                )
            )
            rank_seed += 1
            seen.add(key)
            if len(filtered) >= top_k:
                break

    reranked = []
    for idx, item in enumerate(filtered, start=1):
        reranked.append(
            RankedItem(
                rank=idx,
                restaurant_name=item.restaurant_name,
                fit_score=item.fit_score,
                explanation=item.explanation,
            )
        )
    return RankedResult(summary=result.summary, recommendations=reranked)


def save_outputs(result: RankedResult, raw_text: str, output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ranked_path = output_dir / "ranked_recommendations.json"
    summary_path = output_dir / "run_summary.json"
    raw_path = output_dir / "raw_llm_response.txt"

    ranked_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
    summary = {
        "recommendation_count": len(result.recommendations),
        "top_restaurant": result.recommendations[0].restaurant_name if result.recommendations else None,
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    raw_path.write_text(raw_text, encoding="utf-8")

    return {
        "ranked_recommendations": str(ranked_path),
        "run_summary": str(summary_path),
        "raw_llm_response": str(raw_path),
    }

