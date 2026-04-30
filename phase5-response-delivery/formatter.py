from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class RecommendationCard:
    rank: int
    restaurant_name: str
    cuisine: str
    rating: float | None
    estimated_cost_for_two: float | None
    ai_explanation: str


@dataclass(frozen=True)
class FormattedResponse:
    generated_at_utc: str
    total_results: int
    recommendations: list[RecommendationCard]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _to_float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def format_recommendation_payload(ranked_payload: dict[str, Any], top_k: int = 5) -> FormattedResponse:
    rows = ranked_payload.get("recommendations", [])
    if not isinstance(rows, list):
        rows = []

    cards: list[RecommendationCard] = []
    for idx, row in enumerate(rows[:top_k], start=1):
        cards.append(
            RecommendationCard(
                rank=int(row.get("rank", idx)),
                restaurant_name=str(row.get("restaurant_name", "Unknown")).strip(),
                cuisine=str(row.get("cuisine", "Not specified")).strip(),
                rating=_to_float_or_none(row.get("rating")),
                estimated_cost_for_two=_to_float_or_none(row.get("estimated_cost_for_two")),
                ai_explanation=str(row.get("explanation", "No explanation available.")).strip(),
            )
        )

    return FormattedResponse(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        total_results=len(cards),
        recommendations=cards,
    )

