# Phase 2 Preference Capture Layer

This folder contains a separate implementation of **Phase 2: User Preference Capture Layer** from `docs/problemstatement.md`.

## Scope

- Form-based user input collection (basic web UI)
- Validation of user preferences
- Normalization into a machine-friendly preference object
- JSON output of normalized preferences for downstream filtering

## Captured fields

- Location
- Budget (`low`, `medium`, `high`)
- Cuisine
- Minimum rating (`0.0` to `5.0`)
- Additional preferences (free text)

## Outputs

- `phase2-preference-capture/data/normalized_preferences.json`

## Run

From project root:

```bash
pip install -r requirements.txt
python phase2-preference-capture/app.py
```

Open:

- [http://127.0.0.1:5001/](http://127.0.0.1:5001/)

