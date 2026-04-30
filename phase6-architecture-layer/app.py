from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request

from contracts import parse_request_payload
from env_loader import load_env_file
from orchestrator import run_end_to_end

app = Flask(__name__)
load_env_file(Path(__file__).resolve().parents[1] / ".env")


@app.post("/api/v1/recommendations")
def recommendations():
    payload = request.get_json(silent=True) or {}
    try:
        parsed = parse_request_payload(payload)
        response = run_end_to_end(parsed)
        return jsonify(response)
    except Exception as exc:
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 400


@app.get("/health")
def health():
    return {"status": "ok", "phase": 6}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)

