# Render Backend Deployment

Render is used to host the FastAPI backend.

## Step-by-Step Instructions

1. **Create a New Web Service**:
   - Go to your Render Dashboard and click **New > Web Service**.
   - Connect your GitHub repository.

2. **Configure Service Settings**:
   - **Name**: `reco-partner-backend`
   - **Environment**: `Python 3`
   - **Root Directory**: `.` (leave as root)
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**:
   Click on the **Advanced** button or go to the **Environment** tab:
   - `GROQ_API_KEY`: Your API key for Groq.
   - `PYTHON_VERSION`: `3.10.0` (or your preferred version).

4. **Auto-Deployment**:
   Render will automatically deploy whenever you push to the connected branch (usually `main`).

## Troubleshooting

- **CORS Issues**: Ensure the backend `main.py` has `CORSMiddleware` configured. Currently, it allows all origins (`*`).
- **Memory Limits**: The recommendation pipeline (especially with Pandas) may require a higher tier if the dataset grows significantly.
- **Port**: Render uses the `$PORT` environment variable. The start command handles this automatically.
