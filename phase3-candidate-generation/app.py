from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, render_template, request

from engine import generate_candidates, load_dataset, parse_preferences, save_outputs

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET = BASE_DIR.parent / "phase1-foundation" / "data" / "processed" / "restaurants_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "data"

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", result=None, errors=[])


@app.post("/run")
def run():
    payload = {
        "location": request.form.get("location", ""),
        "budget": request.form.get("budget", ""),
        "cuisine": request.form.get("cuisine", ""),
        "minimum_rating": request.form.get("minimum_rating", ""),
        "additional_preferences": request.form.get("additional_preferences", ""),
    }
    dataset_path = request.form.get("dataset_path", "").strip() or str(DEFAULT_DATASET)

    errors: list[str] = []
    try:
        pref = parse_preferences(payload)
    except Exception as exc:
        errors.append(str(exc))
        return render_template("index.html", result=None, errors=errors)

    try:
        frame = load_dataset(Path(dataset_path))
        candidates, summary = generate_candidates(frame, pref, top_n=30)
        output_paths = save_outputs(candidates, summary, OUTPUT_DIR)
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
        return render_template("index.html", result=None, errors=errors)

    result = {
        "preferences": {
            "location": pref.location,
            "budget": pref.budget,
            "cuisine_tokens": pref.cuisine_tokens,
            "minimum_rating": pref.minimum_rating,
            "additional_tags": pref.additional_tags,
        },
        "summary": summary.to_dict(),
        "output_paths": output_paths,
        "preview": candidates.head(10).to_dict(orient="records"),
    }
    return render_template("index.html", result=result, errors=[])


@app.get("/api/run-from-json")
def run_from_json():
    prefs_path = request.args.get("preferences_path", "").strip()
    dataset_path = request.args.get("dataset_path", "").strip() or str(DEFAULT_DATASET)
    if not prefs_path:
        return {"error": "preferences_path query parameter is required"}, 400

    try:
        payload = json.loads(Path(prefs_path).read_text(encoding="utf-8"))
        pref = parse_preferences(payload)
        frame = load_dataset(Path(dataset_path))
        candidates, summary = generate_candidates(frame, pref, top_n=30)
        output_paths = save_outputs(candidates, summary, OUTPUT_DIR)
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}, 500

    return {
        "preferences": {
            "location": pref.location,
            "budget": pref.budget,
            "cuisine_tokens": pref.cuisine_tokens,
            "minimum_rating": pref.minimum_rating,
            "additional_tags": pref.additional_tags,
        },
        "summary": summary.to_dict(),
        "output_paths": output_paths,
        "candidate_count": len(candidates),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)

