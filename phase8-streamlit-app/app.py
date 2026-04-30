import streamlit as st
import pandas as pd
import sys
import json
from pathlib import Path
from time import perf_counter
from dotenv import load_dotenv

# Load environment variables
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "phase3-candidate-generation"))
sys.path.insert(0, str(ROOT / "phase4-llm-ranking"))
sys.path.insert(0, str(ROOT / "phase5-response-delivery"))
sys.path.insert(0, str(ROOT / "phase6-architecture-layer"))

# Import backend logic
from orchestrator import _load_modules, PHASE1_DATASET
from contracts import PreferenceRequest

# Page Config
st.set_page_config(
    page_title="Reco Partner - AI Restaurant Discovery",
    page_icon="🍴",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #FAFAFA;
    }
    .stButton>button {
        width: 100%;
        background-color: #C41E3A !important;
        color: white !important;
        font-weight: bold !important;
        padding: 0.75rem !important;
        border-radius: 1rem !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #A01830 !important;
        box-shadow: 0 10px 20px -10px rgba(196, 30, 58, 0.4);
    }
    .restaurant-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 1.5rem;
        border: 1px solid #E5E5E5;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .restaurant-card:hover {
        border-color: #C41E3A;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1);
    }
    .rank-badge {
        background-color: #C41E3A;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 0.5rem;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .ai-explanation {
        background-color: #FFF5F5;
        padding: 1rem;
        border-radius: 1rem;
        font-size: 0.9rem;
        color: #4A4A4A;
        border-left: 4px solid #C41E3A;
    }
    .price-tag {
        color: #1A1A1A;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .rating-badge {
        background-color: #166534;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.4rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🍴 Reco Partner")
st.markdown("### AI-Powered Restaurant Recommendations")
st.markdown("---")

# Load Data for Options
@st.cache_data
def get_options():
    df = pd.read_csv(PHASE1_DATASET)
    locations = sorted(df['location'].dropna().unique().tolist())
    return locations

locations = get_options()

# Sidebar Inputs
with st.sidebar:
    st.header("Your Preferences")
    
    location = st.selectbox("Your Location", options=locations, index=locations.index("indiranagar") if "indiranagar" in locations else 0)
    
    budget = st.radio("Budget Range", options=["low", "medium", "high"], index=1)
    
    cuisines_list = ["Italian", "North Indian", "Chinese", "Japanese", "Mediterranean", "French", "Mexican"]
    selected_cuisines = st.multiselect("Favorite Cuisines", options=cuisines_list, default=["Italian", "Chinese"])
    
    min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=3.5, step=0.1)
    
    vibe = st.selectbox("Vibe & Occasion", options=["Family-friendly", "Romantic", "Business", "Nightlife"])
    
    additional_prefs = st.text_area("Additional Preferences", placeholder="e.g., outdoor seating, pet-friendly, quick service")
    
    # top_k is now hardcoded to 5 as per user request
    top_k = 5

# Main logic
if st.button("Find Best Matches"):
    if not selected_cuisines:
        st.error("Please select at least one cuisine.")
    else:
        with st.spinner("Analyzing top restaurants for you..."):
            try:
                # Prepare Request
                request = PreferenceRequest(
                    location=location,
                    budget=budget,
                    cuisine=", ".join(selected_cuisines),
                    minimum_rating=min_rating,
                    additional_preferences=vibe + (f", {additional_prefs}" if additional_prefs else ""),
                    top_k=top_k
                )
                
                # Load modules
                modules = _load_modules()
                
                # Execute Pipeline (direct call to backend logic)
                started = perf_counter()
                
                # Data
                frame = modules["load_dataset"](PHASE1_DATASET)
                
                # Preferences
                phase3_prefs = modules["parse_preferences"]({
                    "location": request.location,
                    "budget": request.budget,
                    "cuisine": request.cuisine,
                    "minimum_rating": request.minimum_rating,
                    "additional_preferences": request.additional_preferences,
                })
                
                # Candidates
                candidates_df, phase3_summary = modules["generate_candidates"](frame, phase3_prefs, top_n=30)
                candidates = json.loads(candidates_df.to_json(orient="records"))
                
                if not candidates:
                    st.warning("No candidates found even after relaxing constraints. Try different preferences.")
                else:
                    # Ranking
                    prompt = modules["build_ranking_prompt"](
                        {
                            "location": request.location.lower(),
                            "budget": request.budget,
                            "cuisine_tokens": [x.strip().lower() for x in request.cuisine.split(",") if x.strip()],
                            "minimum_rating": request.minimum_rating,
                            "additional_tags": [x.strip().lower() for x in request.additional_preferences.split(",") if x.strip()],
                        },
                        candidates,
                        top_k=request.top_k,
                    )
                    
                    raw_llm = modules["run_groq_completion"](prompt, model=request.llm_model)
                    
                    try:
                        parsed = modules["parse_ranked_result"](raw_llm)
                    except Exception:
                        # Simple repair attempt
                        repair_prompt = f"Convert to JSON: {raw_llm}"
                        repaired_raw = modules["run_groq_completion"](repair_prompt, model=request.llm_model)
                        parsed = modules["parse_ranked_result"](repaired_raw)
                        
                    validated = modules["validate_against_candidates"](parsed, candidates, top_k=request.top_k)
                    
                    # Final Formatting
                    ranked_payload = validated.to_dict()
                    enriched = modules["enrich_ranked_payload"](ranked_payload, candidates)
                    formatted = modules["format_recommendation_payload"](enriched, top_k=request.top_k)
                    results = formatted.to_dict()["recommendations"]
                    
                    elapsed = round((perf_counter() - started) * 1000, 2)
                    
                    # Display Results
                    st.success(f"Found {len(results)} matches")
                    
                    for i, res in enumerate(results):
                        with st.container():
                            st.markdown(f"""
                                <div class="restaurant-card">
                                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                                        <h4 style="margin: 0; color: #1A1A1A;">{res['restaurant_name']}</h4>
                                        <span class="rank-badge">#{res['rank']}</span>
                                    </div>
                                    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 1rem;">
                                        <span class="rating-badge">★ {res['rating'] if res['rating'] else 'N/A'}</span>
                                        <span class="price-tag">₹{res['estimated_cost_for_two']} for two</span>
                                        <span style="color: #888888; font-size: 0.8rem;">• {res['cuisine']}</span>
                                    </div>
                                    <div class="ai-explanation">
                                        <strong>✨ AI Analysis:</strong><br/>
                                        {res['ai_explanation']}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888888; font-size: 0.8rem;'>© 2026 Reco Partner. Powered by Groq LLM.</p>", unsafe_allow_html=True)
