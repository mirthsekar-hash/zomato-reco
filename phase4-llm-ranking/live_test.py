from __future__ import annotations

import json
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PHASE3_DIR = ROOT / "phase3-candidate-generation"
PHASE4_DIR = ROOT / "phase4-llm-ranking"
ENV_PATH = ROOT / ".env"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def main() -> int:
    _load_env_file(ENV_PATH)

    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY is missing. Add it to .env or environment.")
        return 1

    sys.path.insert(0, str(PHASE3_DIR))
    sys.path.insert(0, str(PHASE4_DIR))

    from engine import generate_candidates, load_dataset, parse_preferences, save_outputs as save_phase3_outputs
    from llm_client import DEFAULT_MODEL, run_groq_completion
    from postprocess import parse_ranked_result, save_outputs as save_phase4_outputs, validate_against_candidates
    from prompt_builder import build_ranking_prompt

    dataset_path = ROOT / "phase1-foundation" / "data" / "processed" / "restaurants_cleaned.csv"

    # Budget input from user is numeric (2000). Map it to Phase 3 bucket semantics.
    # >1200 is considered "high" by the candidate generator.
    preferences_payload = {
        "location": "Bellandur",
        "budget": "high",
        "cuisine": "north indian, chinese, biryani",
        "minimum_rating": "4.0",
        "additional_preferences": "",
    }

    frame = load_dataset(dataset_path)
    prefs = parse_preferences(preferences_payload)
    candidates, phase3_summary = generate_candidates(frame, prefs, top_n=30)
    save_phase3_outputs(candidates, phase3_summary, ROOT / "phase3-candidate-generation" / "data")

    candidates_json = json.loads(candidates.to_json(orient="records"))
    prompt = build_ranking_prompt(
        {
            "location": "bellandur",
            "budget": "approximately 2000 for two (high budget bucket)",
            "cuisine_tokens": ["north indian", "chinese", "biryani"],
            "minimum_rating": 4.0,
            "additional_tags": [],
        },
        candidates_json,
        top_k=5,
    )

    raw = run_groq_completion(prompt, model=os.getenv("GROQ_MODEL", DEFAULT_MODEL))
    parsed = parse_ranked_result(raw)
    validated = validate_against_candidates(parsed, candidates_json, top_k=5)
    save_phase4_outputs(validated, raw, ROOT / "phase4-llm-ranking" / "data")

    print(json.dumps(validated.to_dict(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

