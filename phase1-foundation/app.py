from __future__ import annotations

import json
from flask import Flask, render_template, request

from pipeline import run_pipeline, save_preferences

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", result=None, error=None)


@app.post("/run-foundation")
def run_foundation():
    preferences = {
        "location": request.form.get("location", "").strip(),
        "budget": request.form.get("budget", "").strip(),
        "cuisine": request.form.get("cuisine", "").strip(),
        "minimum_rating": request.form.get("minimum_rating", "").strip(),
        "additional_preferences": request.form.get("additional_preferences", "").strip(),
    }

    save_preferences(preferences)
    try:
        pipeline_result = run_pipeline()
        return render_template(
            "index.html",
            result={
                "preferences": preferences,
                "pipeline_result": pipeline_result,
            },
            error=None,
        )
    except Exception as exc:
        return render_template("index.html", result=None, error=f"{type(exc).__name__}: {exc}")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/last-run")
def last_run():
    try:
        from pipeline import OUTPUT_CSV, QUALITY_REPORT, PREFERENCES_FILE

        payload = {
            "preferences_file_exists": PREFERENCES_FILE.exists(),
            "output_csv_exists": OUTPUT_CSV.exists(),
            "quality_report_exists": QUALITY_REPORT.exists(),
        }
        if QUALITY_REPORT.exists():
            payload["quality_report"] = json.loads(QUALITY_REPORT.read_text(encoding="utf-8"))
        return payload
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}, 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

