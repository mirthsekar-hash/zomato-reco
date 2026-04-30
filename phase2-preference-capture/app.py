from __future__ import annotations

from flask import Flask, render_template, request

from normalizer import normalize_preferences
from preference_schema import RawPreferences
from storage import save_normalized_preferences
from validator import validate_preferences

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", errors=[], result=None)


@app.post("/submit")
def submit():
    raw = RawPreferences(
        location=request.form.get("location", ""),
        budget=request.form.get("budget", ""),
        cuisine=request.form.get("cuisine", ""),
        minimum_rating=request.form.get("minimum_rating", ""),
        additional_preferences=request.form.get("additional_preferences", ""),
    )

    validation = validate_preferences(raw)
    if not validation.is_valid:
        return render_template("index.html", errors=validation.errors, result=None)

    normalized = normalize_preferences(raw)
    output_path = save_normalized_preferences(normalized)

    return render_template(
        "index.html",
        errors=[],
        result={
            "normalized_preferences": normalized.to_dict(),
            "output_path": output_path,
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)

