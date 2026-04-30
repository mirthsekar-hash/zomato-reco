# Phase 1 Foundation

This folder contains a separate implementation of **Phase 1: Foundation and Data Preparation** from `docs/problemstatement.md`.

## What this includes

- Dataset ingestion from Hugging Face (`ManikaSaini/zomato-restaurant-recommendation`)
- Data preprocessing and standardization
- Curated, query-ready output dataset
- Data quality report generation
- Basic web UI input source (form) to capture user preferences

## Output files

- `phase1-foundation/data/processed/restaurants_cleaned.csv`
- `phase1-foundation/data/processed/quality_report.json`
- `phase1-foundation/data/processed/last_preferences.json`

## Run

From project root:

```bash
pip install -r requirements.txt
python phase1-foundation/app.py
```

Open:

- [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

