from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_candidate_index(candidates_payload: list[dict]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for row in candidates_payload:
        name = str(row.get("name", "")).strip()
        if not name:
            continue
        index[name.lower()] = row
    return index


def enrich_ranked_payload(ranked_payload: dict, candidates_payload: list[dict]) -> dict:
    index = build_candidate_index(candidates_payload)
    rows = ranked_payload.get("recommendations", [])
    if not isinstance(rows, list):
        return ranked_payload

    enriched_rows: list[dict] = []
    for row in rows:
        name = str(row.get("restaurant_name", "")).strip()
        candidate = index.get(name.lower(), {})
        enriched_rows.append(
            {
                **row,
                "cuisine": candidate.get("cuisines", row.get("cuisine")),
                "rating": candidate.get("rating", row.get("rating")),
                "estimated_cost_for_two": candidate.get("estimated_cost_for_two", row.get("estimated_cost_for_two")),
            }
        )

    return {**ranked_payload, "recommendations": enriched_rows}

