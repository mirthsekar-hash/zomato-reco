from __future__ import annotations

import json


def build_ranking_prompt(preferences: dict, candidates: list[dict], top_k: int) -> str:
    compact_candidates: list[dict] = []
    for row in candidates:
        compact_candidates.append(
            {
                "name": row.get("name"),
                "location": row.get("location"),
                "cuisines": row.get("cuisines"),
                "estimated_cost_for_two": row.get("estimated_cost_for_two"),
                "rating": row.get("rating"),
                "candidate_score": row.get("candidate_score"),
            }
        )

    instruction = {
        "task": "Rank restaurant candidates for user preference fit and explain each choice.",
        "rules": [
            "Only use restaurants provided in the candidates list. Do not invent names.",
            "Respect preference constraints: location, budget, cuisine, and minimum_rating.",
            "If a field is missing in candidate data, do not fabricate details.",
            "Prefer deterministic ordering by fit quality.",
            f"Return exactly top {top_k} items unless fewer candidates are provided.",
        ],
        "output_schema": {
            "summary": "string",
            "recommendations": [
                {
                    "rank": "integer",
                    "restaurant_name": "string",
                    "fit_score": "number_0_to_10",
                    "explanation": "string_under_60_words",
                }
            ],
        },
    }

    payload = {
        "preferences": preferences,
        "candidates": compact_candidates,
    }

    return (
        "You are a restaurant recommendation ranking assistant.\n"
        "Follow instructions exactly and return valid JSON only.\n\n"
        f"INSTRUCTION:\n{json.dumps(instruction, indent=2)}\n\n"
        f"INPUT:\n{json.dumps(payload, indent=2)}\n"
    )

