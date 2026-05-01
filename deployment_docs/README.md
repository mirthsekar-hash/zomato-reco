# Reco Partner Deployment Documentation

This directory contains instructions and references for deploying the Reco Partner application with a split architecture:

- **Backend**: Python (FastAPI) deployed on [Railway](https://railway.app)
- **Frontend**: Next.js (TypeScript) deployed on [Vercel](https://vercel.com)

## Architecture Overview

The application is split into two independent services:
1. **Backend**: Handles data processing, candidate generation, and LLM ranking.
2. **Frontend**: Provides a premium UI for users to interact with the recommendation engine.

## Documentation Index

1. [Railway Backend Setup](./railway_setup.md)

2. [Vercel Frontend Setup](./vercel_setup.md)
3. [API Reference](./api_reference.md)
4. [Environment Variables](./env_vars.md)

## Local Development

To run the full stack locally:

### 1. Start Backend
```bash
# From the project root
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
The backend will run at `http://localhost:8000`.

### 2. Start Frontend
```bash
# From frontend-ui directory
npm install
npm run dev
```
The frontend will run at `http://localhost:3000`. Ensure `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`.
