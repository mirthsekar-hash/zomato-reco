# Environment Variables Reference

A summary of all environment variables required for the Reco Partner stack.

## Backend (Railway)

| Variable | Required | Description | Example |
| :--- | :--- | :--- | :--- |
| `GROQ_API_KEY` | **Yes** | Your API key for Groq LLM. | `gsk_...` |
| `PORT` | No | Port for the FastAPI server (Set by Railway). | `8000` |
| `PYTHON_VERSION` | No | Specifies Python version to use. | `3.10.0` |


---

## Frontend (Vercel)

| Variable | Required | Description | Example |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | **Yes** | The base URL of the backend API. | `https://api.reco.com` |

---

## Local Development (.env files)

### Root `.env` (Backend)
```env
GROQ_API_KEY=your_key_here
```

### `frontend-ui/.env.local` (Frontend)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```
