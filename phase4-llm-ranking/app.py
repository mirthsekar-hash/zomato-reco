from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, render_template, request

from llm_client import DEFAULT_MODEL, run_groq_completion
from postprocess import parse_ranked_result, save_outputs, validate_against_candidates
from prompt_builder import build_ranking_prompt

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CANDIDATES = BASE_DIR.parent / "phase3-candidate-generation" / "data" / "candidates.json"
OUTPUT_DIR = BASE_DIR / "data"

app = Flask(__name__)


def _load_candidates(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Candidates file not found: {path}")
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("Candidates file must contain a JSON list.")
    if not rows:
        raise ValueError("Candidates list is empty.")
    return rows


def _build_preferences_from_form(form) -> dict:
    return {
        "location": form.get("location", "").strip().lower(),
        "budget": form.get("budget", "").strip().lower(),
        "cuisine_tokens": sorted(
            {
                item.strip().lower()
                for item in (form.get("cuisine", "") or "").replace("/", ",").split(",")
                if item.strip()
            }
        ),
        "minimum_rating": float(form.get("minimum_rating", "0") or 0),
        "additional_tags": sorted(
            {
                item.strip().lower()
                for item in (form.get("additional_preferences", "") or "").replace("/", ",").split(",")
                if item.strip()
            }
        ),
    }


@app.get("/")
def index():
    return render_template("index.html", errors=[], result=None, default_model=DEFAULT_MODEL)


@app.post("/run")
def run():
    errors: list[str] = []
    candidates_path = request.form.get("candidates_path", "").strip() or str(DEFAULT_CANDIDATES)
    model = request.form.get("model", "").strip() or DEFAULT_MODEL
    top_k_text = request.form.get("top_k", "5").strip()

    try:
        top_k = int(top_k_text)
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0.")
    except Exception:
        errors.append("top_k must be a positive integer.")
        return render_template("index.html", errors=errors, result=None, default_model=DEFAULT_MODEL)

    try:
        preferences = _build_preferences_from_form(request.form)
    except Exception as exc:
        errors.append(f"Invalid preference input: {exc}")
        return render_template("index.html", errors=errors, result=None, default_model=DEFAULT_MODEL)

    try:
        candidates = _load_candidates(Path(candidates_path))
        prompt = build_ranking_prompt(preferences, candidates, top_k=top_k)
        raw_text = run_groq_completion(prompt, model=model)
        parsed = parse_ranked_result(raw_text)
        validated = validate_against_candidates(parsed, candidates, top_k=top_k)
        paths = save_outputs(validated, raw_text, OUTPUT_DIR)
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
        return render_template("index.html", errors=errors, result=None, default_model=DEFAULT_MODEL)

    result = {
        "model": model,
        "top_k": top_k,
        "summary": validated.summary,
        "recommendations": [r.__dict__ for r in validated.recommendations],
        "output_paths": paths,
    }
    return render_template("index.html", errors=[], result=result, default_model=DEFAULT_MODEL)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=True)

