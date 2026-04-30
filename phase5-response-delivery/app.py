from __future__ import annotations

from pathlib import Path
from time import perf_counter

from flask import Flask, jsonify, render_template, request

from data_source import enrich_ranked_payload, load_json
from formatter import format_recommendation_payload

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_RANKED_PATH = BASE_DIR.parent / "phase4-llm-ranking" / "data" / "ranked_recommendations.json"
DEFAULT_CANDIDATES_PATH = BASE_DIR.parent / "phase3-candidate-generation" / "data" / "candidates.json"

app = Flask(__name__)


def _parse_top_k(raw: str | None, default: int = 5) -> int:
    if not raw:
        return default
    try:
        value = int(raw)
        return value if value > 0 else default
    except ValueError:
        return default


@app.get("/api/recommendations")
def api_recommendations():
    start = perf_counter()
    ranked_path = request.args.get("ranked_path", "").strip() or str(DEFAULT_RANKED_PATH)
    candidates_path = request.args.get("candidates_path", "").strip() or str(DEFAULT_CANDIDATES_PATH)
    top_k = _parse_top_k(request.args.get("top_k", "5"), default=5)

    try:
        ranked_payload = load_json(Path(ranked_path))
        candidates_payload = load_json(Path(candidates_path))
        enriched = enrich_ranked_payload(ranked_payload, candidates_payload)
        formatted = format_recommendation_payload(enriched, top_k=top_k)
        response = formatted.to_dict()
        response["meta"] = {
            "ranked_path": ranked_path,
            "candidates_path": candidates_path,
            "response_time_ms": round((perf_counter() - start) * 1000, 2),
        }
        return jsonify(response)
    except Exception as exc:
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500


@app.get("/")
def index():
    ranked_path = request.args.get("ranked_path", "").strip() or str(DEFAULT_RANKED_PATH)
    candidates_path = request.args.get("candidates_path", "").strip() or str(DEFAULT_CANDIDATES_PATH)
    top_k = _parse_top_k(request.args.get("top_k", "5"), default=5)

    error = None
    cards = []
    meta = {}
    summary_text = ""

    start = perf_counter()
    try:
        ranked_payload = load_json(Path(ranked_path))
        candidates_payload = load_json(Path(candidates_path))
        enriched = enrich_ranked_payload(ranked_payload, candidates_payload)
        formatted = format_recommendation_payload(enriched, top_k=top_k)
        cards = formatted.recommendations
        summary_text = str(ranked_payload.get("summary", "")).strip()
        meta = {
            "total_results": formatted.total_results,
            "generated_at_utc": formatted.generated_at_utc,
            "response_time_ms": round((perf_counter() - start) * 1000, 2),
        }
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"

    return render_template(
        "index.html",
        cards=cards,
        error=error,
        summary_text=summary_text,
        meta=meta,
        ranked_path=ranked_path,
        candidates_path=candidates_path,
        top_k=top_k,
    )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5004, debug=True)

