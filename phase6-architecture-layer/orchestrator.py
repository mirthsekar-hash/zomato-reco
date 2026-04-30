from __future__ import annotations

import json
from pathlib import Path
import sys
from time import perf_counter
from typing import Any

from contracts import PreferenceRequest


ROOT = Path(__file__).resolve().parents[1]
PHASE1_DATASET = ROOT / "phase1-foundation" / "data" / "processed" / "restaurants_cleaned.csv"


def _load_modules():
    sys.path.insert(0, str(ROOT / "phase3-candidate-generation"))
    sys.path.insert(0, str(ROOT / "phase4-llm-ranking"))
    sys.path.insert(0, str(ROOT / "phase5-response-delivery"))

    from engine import generate_candidates, load_dataset, parse_preferences  # type: ignore
    from llm_client import run_groq_completion  # type: ignore
    from prompt_builder import build_ranking_prompt  # type: ignore
    from postprocess import parse_ranked_result, validate_against_candidates  # type: ignore
    from data_source import enrich_ranked_payload  # type: ignore
    from formatter import format_recommendation_payload  # type: ignore

    return {
        "load_dataset": load_dataset,
        "parse_preferences": parse_preferences,
        "generate_candidates": generate_candidates,
        "build_ranking_prompt": build_ranking_prompt,
        "run_groq_completion": run_groq_completion,
        "parse_ranked_result": parse_ranked_result,
        "validate_against_candidates": validate_against_candidates,
        "enrich_ranked_payload": enrich_ranked_payload,
        "format_recommendation_payload": format_recommendation_payload,
    }


def run_end_to_end(request: PreferenceRequest) -> dict[str, Any]:
    modules = _load_modules()
    started = perf_counter()

    frame = modules["load_dataset"](PHASE1_DATASET)
    phase3_prefs = modules["parse_preferences"](
        {
            "location": request.location,
            "budget": request.budget,
            "cuisine": request.cuisine,
            "minimum_rating": request.minimum_rating,
            "additional_preferences": request.additional_preferences,
        }
    )
    candidates_df, phase3_summary = modules["generate_candidates"](frame, phase3_prefs, top_n=30)
    candidates = json.loads(candidates_df.to_json(orient="records"))

    prompt = modules["build_ranking_prompt"](
        {
            "location": request.location.lower(),
            "budget": request.budget,
            "cuisine_tokens": [x.strip().lower() for x in request.cuisine.split(",") if x.strip()],
            "minimum_rating": request.minimum_rating,
            "additional_tags": [x.strip().lower() for x in request.additional_preferences.split(",") if x.strip()],
        },
        candidates,
        top_k=request.top_k,
    )
    raw_llm = modules["run_groq_completion"](prompt, model=request.llm_model)
    try:
        parsed = modules["parse_ranked_result"](raw_llm)
    except Exception:
        repair_prompt = (
            "Convert the following text into valid JSON only with keys "
            "'summary' and 'recommendations'. Do not add markdown.\n\n"
            f"{raw_llm}"
        )
        repaired_raw = modules["run_groq_completion"](repair_prompt, model=request.llm_model)
        parsed = modules["parse_ranked_result"](repaired_raw)
    validated = modules["validate_against_candidates"](parsed, candidates, top_k=request.top_k)

    ranked_payload = validated.to_dict()
    enriched = modules["enrich_ranked_payload"](ranked_payload, candidates)
    formatted = modules["format_recommendation_payload"](enriched, top_k=request.top_k)
    response = formatted.to_dict()
    response["meta"] = {
        "phase3_fallback_stage": phase3_summary.fallback_stage,
        "phase3_output_rows": phase3_summary.output_rows,
        "llm_model": request.llm_model,
        "response_time_ms": round((perf_counter() - started) * 1000, 2),
    }
    return response

