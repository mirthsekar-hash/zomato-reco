from __future__ import annotations

import json
from pathlib import Path

from preference_schema import NormalizedPreferences

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data"
OUTPUT_FILE = OUTPUT_DIR / "normalized_preferences.json"


def save_normalized_preferences(preferences: NormalizedPreferences) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = preferences.to_dict()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(OUTPUT_FILE)

