# Phase 3 Candidate Generation

This folder contains a separate implementation of **Phase 3: Retrieval and Candidate Generation** from `docs/problemstatement.md`.

## Scope

- Load cleaned dataset from Phase 1
- Accept normalized preferences (from Phase 2 style object)
- Apply hard constraints (location, budget, minimum rating, cuisine)
- Produce top matching candidates for downstream LLM ranking
- Use fallback relaxation when strict filtering returns few/no results

## Inputs

- `phase1-foundation/data/processed/restaurants_cleaned.csv`
- Preference input from web UI (or optional JSON file path)

## Outputs

- `phase3-candidate-generation/data/candidates.csv`
- `phase3-candidate-generation/data/candidates.json`
- `phase3-candidate-generation/data/last_run_summary.json`

## Run

```bash
pip install -r requirements.txt
python phase3-candidate-generation/app.py
```

Open:

- [http://127.0.0.1:5002/](http://127.0.0.1:5002/)

