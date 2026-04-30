# Phase 5 Response Delivery and Presentation

This folder contains a separate implementation of **Phase 5: Response Delivery and Presentation** from `docs/problemstatement.md`.

## Scope

- Recommendation API to serve ranked results
- Response formatter to enforce stable output schema
- User-facing presentation layer (web UI) for recommendation cards
- Basic performance metadata in API response

## Default input source

- `phase4-llm-ranking/data/ranked_recommendations.json`

## Run

```bash
pip install -r requirements.txt
python phase5-response-delivery/app.py
```

Open:

- UI: [http://127.0.0.1:5004/](http://127.0.0.1:5004/)
- API: [http://127.0.0.1:5004/api/recommendations](http://127.0.0.1:5004/api/recommendations)

