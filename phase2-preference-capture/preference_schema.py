from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RawPreferences:
    location: str
    budget: str
    cuisine: str
    minimum_rating: str
    additional_preferences: str


@dataclass(frozen=True)
class NormalizedPreferences:
    location: str
    budget: str
    cuisine_tokens: list[str]
    minimum_rating: float
    additional_tags: list[str]

    def to_dict(self) -> dict:
        return asdict(self)

