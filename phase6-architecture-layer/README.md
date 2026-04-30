# Phase 6: Updated Backend and Frontend Architecture

This folder implements **Phase 6** from `docs/problemstatement.md` as a contract-driven integration layer between frontend and backend services.

## Purpose

- Define a stable API contract between UI and backend
- Validate frontend request payloads
- Orchestrate backend flow across:
  - Phase 3 candidate generation
  - Phase 4 Groq LLM ranking
  - Phase 5 response formatting
- Return a single frontend-ready response

## API

- `POST /api/v1/recommendations`
  - Input: normalized user preference payload
  - Output: formatted recommendation response schema
- `GET /health`

## Run

```bash
pip install -r requirements.txt
python phase6-architecture-layer/app.py
```

Open:

- `http://127.0.0.1:5005/health`

