from __future__ import annotations

from dataclasses import dataclass

from preference_schema import RawPreferences


BUDGET_ALIASES = {
    "low": "low",
    "budget": "low",
    "cheap": "low",
    "economy": "low",
    "medium": "medium",
    "mid": "medium",
    "moderate": "medium",
    "high": "high",
    "premium": "high",
    "expensive": "high",
}


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: list[str]


def _has_content(value: str) -> bool:
    return bool(value and value.strip())


def _validate_rating(rating_text: str) -> tuple[bool, str | None]:
    try:
        value = float(rating_text)
    except ValueError:
        return False, "Minimum rating must be a number between 0 and 5."
    if value < 0 or value > 5:
        return False, "Minimum rating must be within the 0 to 5 range."
    return True, None


def validate_preferences(raw: RawPreferences) -> ValidationResult:
    errors: list[str] = []

    if not _has_content(raw.location):
        errors.append("Location is required.")
    if not _has_content(raw.cuisine):
        errors.append("Cuisine is required.")
    if not _has_content(raw.budget):
        errors.append("Budget is required.")
    else:
        normalized_budget = raw.budget.strip().lower()
        if normalized_budget not in BUDGET_ALIASES:
            errors.append("Budget must be one of: low, medium, high (or known synonyms).")

    if not _has_content(raw.minimum_rating):
        errors.append("Minimum rating is required.")
    else:
        rating_ok, rating_error = _validate_rating(raw.minimum_rating.strip())
        if not rating_ok and rating_error:
            errors.append(rating_error)

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)

