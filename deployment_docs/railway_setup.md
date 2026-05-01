# Railway Backend Deployment

Railway is used to host the FastAPI backend.

## Step-by-Step Instructions

1. **Create a New Project**:
   - Go to your [Railway Dashboard](https://railway.app) and click **New Project**.
   - Select **Deploy from GitHub repo**.
   - Connect your repository.

2. **Configure Service Settings**:
   - Railway will automatically detect the Python environment.
   - It will use the `Procfile` in the root to determine the start command:
     `web: uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}`
   - **Root Directory**: Ensure it is set to the project root (`/`).

3. **Environment Variables**:
   Go to the **Variables** tab of your service:
   - `GROQ_API_KEY`: Your API key for Groq.
   - `PORT`: (Optional) Railway provides this automatically, but you can set it if needed.

4. **Deployment**:
   Railway will deploy automatically on every push to your main branch.

## Troubleshooting

- **Build Failures**: Check the `Build Logs` to ensure all dependencies in `backend/requirements.txt` are installed.
- **Port Binding**: Ensure your code uses the `PORT` environment variable (the `Procfile` handles this).
- **CORS**: Ensure `backend/main.py` has CORS enabled for your Vercel URL.
