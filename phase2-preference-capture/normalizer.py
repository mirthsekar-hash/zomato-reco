from __future__ import annotations

import re

from preference_schema import NormalizedPreferences, RawPreferences
from validator import BUDGET_ALIASES


LOCATION_ALIASES = {
    "bengaluru": "bangalore",
    "banglore": "bangalore",
    "delhi ncr": "delhi",
    "bombay": "mumbai",
}


def _normalize_location(location: str) -> str:
    cleaned = location.strip().lower()
    return LOCATION_ALIASES.get(cleaned, cleaned)


def _normalize_budget(budget: str) -> str:
    cleaned = budget.strip().lower()
    return BUDGET_ALIASES[cleaned]


def _tokenize_list(value: str) -> list[str]:
    items = [part.strip().lower() for part in re.split(r"[,/|]", value) if part.strip()]
    deduped = sorted(set(items))
    return deduped


def normalize_preferences(raw: RawPreferences) -> NormalizedPreferences:
    minimum_rating = round(float(raw.minimum_rating.strip()), 2)
    additional = _tokenize_list(raw.additional_preferences) if raw.additional_preferences.strip() else []

    return NormalizedPreferences(
        location=_normalize_location(raw.location),
        budget=_normalize_budget(raw.budget),
        cuisine_tokens=_tokenize_list(raw.cuisine),
        minimum_rating=minimum_rating,
        additional_tags=additional,
    )

