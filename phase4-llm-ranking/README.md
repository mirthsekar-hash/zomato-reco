# Phase 4 LLM Ranking and Explanation (Groq)

This folder contains a separate implementation of **Phase 4: LLM-Based Ranking and Explanation** from `docs/problemstatement.md`.

## Scope

- Build a structured prompt from user preferences + Phase 3 candidates
- Use **Groq** as the LLM provider for ranking and explanation generation
- Parse and validate LLM output into a stable schema
- Save ranked recommendations and run metadata

## Inputs

- Candidate input JSON (default):
  - `phase3-candidate-generation/data/candidates.json`
- Preferences (from UI form or optional JSON file)

## Outputs

- `phase4-llm-ranking/data/ranked_recommendations.json`
- `phase4-llm-ranking/data/run_summary.json`
- `phase4-llm-ranking/data/raw_llm_response.txt`

## Environment

Set your Groq API key:

- PowerShell: `$env:GROQ_API_KEY="your_key_here"`

Optional model override:

- PowerShell: `$env:GROQ_MODEL="llama-3.1-8b-instant"`

Default model used by app:

- `llama-3.1-8b-instant`

## Run

```bash
pip install -r requirements.txt
python phase4-llm-ranking/app.py
```

Open:

- [http://127.0.0.1:5003/](http://127.0.0.1:5003/)

