from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class PreferenceRequest:
    location: str
    budget: str
    cuisine: str
    minimum_rating: float
    additional_preferences: str = ""
    top_k: int = 5
    llm_model: str = "llama-3.1-8b-instant"


@dataclass(frozen=True)
class ContractResponse:
    generated_at_utc: str
    total_results: int
    recommendations: list[dict[str, Any]]
    meta: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def parse_request_payload(payload: dict[str, Any]) -> PreferenceRequest:
    location = str(payload.get("location", "")).strip()
    budget = str(payload.get("budget", "")).strip().lower()
    cuisine = str(payload.get("cuisine", "")).strip()
    additional = str(payload.get("additional_preferences", "")).strip()

    if not location:
        raise ValueError("location is required.")
    if not budget:
        raise ValueError("budget is required.")
    if not cuisine:
        raise ValueError("cuisine is required.")

    try:
        minimum_rating = float(payload.get("minimum_rating", 0))
    except ValueError as exc:
        raise ValueError("minimum_rating must be numeric.") from exc
    if minimum_rating < 0 or minimum_rating > 5:
        raise ValueError("minimum_rating must be in range 0..5.")

    try:
        top_k = int(payload.get("top_k", 5))
    except ValueError as exc:
        raise ValueError("top_k must be an integer.") from exc
    if top_k <= 0:
        raise ValueError("top_k must be > 0.")

    llm_model = str(payload.get("llm_model", "llama-3.1-8b-instant")).strip()
    if not llm_model:
        llm_model = "llama-3.1-8b-instant"

    return PreferenceRequest(
        location=location,
        budget=budget,
        cuisine=cuisine,
        minimum_rating=round(minimum_rating, 2),
        additional_preferences=additional,
        top_k=top_k,
        llm_model=llm_model,
    )

