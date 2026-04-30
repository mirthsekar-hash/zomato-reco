from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


@dataclass(frozen=True)
class QualityReport:
    row_count: int
    missing_name_count: int
    missing_location_count: int
    missing_cuisine_count: int
    missing_cost_count: int
    missing_rating_count: int
    duplicate_key_count: int
    invalid_rating_count: int
    quality_gate_passed: bool

    def to_dict(self) -> dict:
        return asdict(self)


def build_quality_report(df: pd.DataFrame) -> QualityReport:
    missing_name = int(df["name"].isna().sum())
    missing_location = int(df["location"].isna().sum())
    missing_cuisine = int(df["cuisines"].isna().sum())
    missing_cost = int(df["estimated_cost_for_two"].isna().sum())
    missing_rating = int(df["rating"].isna().sum())

    dedupe_key = (
        df["name"].fillna("").str.lower().str.strip()
        + "|"
        + df["location"].fillna("").str.lower().str.strip()
        + "|"
        + df["cuisines"].fillna("").str.lower().str.strip()
    )
    duplicates = int(dedupe_key.duplicated().sum())
    invalid_rating = int(((df["rating"] < 0) | (df["rating"] > 5)).fillna(False).sum())

    # Basic gate: no missing identity fields and no invalid ratings.
    quality_gate_passed = missing_name == 0 and missing_location == 0 and invalid_rating == 0

    return QualityReport(
        row_count=len(df),
        missing_name_count=missing_name,
        missing_location_count=missing_location,
        missing_cuisine_count=missing_cuisine,
        missing_cost_count=missing_cost,
        missing_rating_count=missing_rating,
        duplicate_key_count=duplicates,
        invalid_rating_count=invalid_rating,
        quality_gate_passed=quality_gate_passed,
    )

