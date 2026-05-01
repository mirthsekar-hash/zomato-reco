import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
from dotenv import load_dotenv

# Setup paths
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

# Add internal modules to path
sys.path.insert(0, str(ROOT / "phase6-architecture-layer"))
from orchestrator import run_end_to_end, PHASE1_DATASET
from contracts import PreferenceRequest as LogicPreferenceRequest

app = FastAPI(title="Reco Partner API", version="1.0.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models for API
class RecommendationRequest(BaseModel):
    location: str
    budget: str
    cuisine: str
    minimum_rating: float = 3.5
    additional_preferences: Optional[str] = ""
    top_k: int = 5
    llm_model: str = "llama-3.1-8b-instant"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "reco-partner-backend"}

@app.get("/api/v1/locations")
def get_locations():
    try:
        df = pd.read_csv(PHASE1_DATASET)
        locations = sorted(df['location'].dropna().unique().tolist())
        return {"locations": locations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading locations: {str(e)}")

@app.post("/api/v1/recommendations")
def get_recommendations(req: RecommendationRequest):
    try:
        # Convert Pydantic model to the logic's PreferenceRequest
        logic_req = LogicPreferenceRequest(
            location=req.location,
            budget=req.budget,
            cuisine=req.cuisine,
            minimum_rating=req.minimum_rating,
            additional_preferences=req.additional_preferences or "",
            top_k=req.top_k,
            llm_model=req.llm_model
        )
        
        result = run_end_to_end(logic_req)
        return result
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
