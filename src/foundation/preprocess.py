from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class StandardColumn:
    canonical: str
    aliases: tuple[str, ...]


STANDARD_COLUMNS = (
    StandardColumn("name", ("restaurant_name", "res_name", "name")),
    StandardColumn("location", ("city", "location", "locality")),
    StandardColumn("cuisines", ("cuisine", "cuisines", "food_type")),
    StandardColumn("average_cost_for_two", ("average_cost_for_two", "cost_for_two", "price_for_two")),
    StandardColumn("aggregate_rating", ("aggregate_rating", "rating", "user_rating")),
)


LOCATION_ALIASES = {
    "bengaluru": "bangalore",
    "banglore": "bangalore",
    "bombay": "mumbai",
    "delhi ncr": "delhi",
}


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map: dict[str, str] = {}
    lower_lookup = {col.lower().strip(): col for col in df.columns}

    for spec in STANDARD_COLUMNS:
        for alias in spec.aliases:
            source = lower_lookup.get(alias.lower())
            if source:
                rename_map[source] = spec.canonical
                break

    standardized = df.rename(columns=rename_map).copy()
    return standardized


def _parse_cost(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    text = str(value).strip().lower()
    if not text:
        return None

    numbers = re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))
    if not numbers:
        return None

    nums = [float(n) for n in numbers]
    return sum(nums) / len(nums)


def normalize_location(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    normalized = str(value).strip().lower()
    if not normalized:
        return None

    return LOCATION_ALIASES.get(normalized, normalized)


def normalize_cuisines(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    raw = str(value).strip()
    if not raw:
        return None

    tokens = [token.strip().lower() for token in re.split(r"[,/|]", raw) if token.strip()]
    deduped = sorted(set(tokens))
    return ", ".join(deduped) if deduped else None


def clamp_rating(value: Any, min_rating: float = 0.0, max_rating: float = 5.0) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    try:
        rating = float(value)
    except (TypeError, ValueError):
        return None

    if rating < min_rating or rating > max_rating:
        return None
    return round(rating, 2)


def preprocess_restaurants(df: pd.DataFrame) -> pd.DataFrame:
    frame = standardize_columns(df)

    for required in ("name", "location", "cuisines", "average_cost_for_two", "aggregate_rating"):
        if required not in frame.columns:
            frame[required] = pd.NA

    frame["name"] = frame["name"].astype(str).str.strip()
    frame["location"] = frame["location"].map(normalize_location)
    frame["cuisines"] = frame["cuisines"].map(normalize_cuisines)
    frame["estimated_cost_for_two"] = frame["average_cost_for_two"].map(_parse_cost)
    frame["rating"] = frame["aggregate_rating"].map(clamp_rating)

    # Remove rows without core identity fields.
    frame = frame.dropna(subset=["name", "location"])
    frame = frame[frame["name"].str.len() > 0]

    # Keep only query-ready curated columns.
    curated = frame[
        ["name", "location", "cuisines", "estimated_cost_for_two", "rating"]
    ].copy()

    # Deduplicate near-identical records using normalized key.
    dedupe_key = (
        curated["name"].str.lower().str.strip()
        + "|"
        + curated["location"].fillna("").str.lower().str.strip()
        + "|"
        + curated["cuisines"].fillna("").str.lower().str.strip()
    )
    curated = curated.loc[~dedupe_key.duplicated()].reset_index(drop=True)
    return curated

