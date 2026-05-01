# API Reference

The backend exposes the following REST API endpoints.

## Base URL
`http://localhost:8000` (Local)
`https://your-app.onrender.com` (Production)

---

## 1. Health Check
`GET /health`

Returns the status of the backend service.

**Response:**
```json
{
  "status": "healthy",
  "service": "reco-partner-backend"
}
```

---

## 2. Get Locations
`GET /api/v1/locations`

Fetches a list of unique restaurant locations from the dataset.

**Response:**
```json
{
  "locations": ["Indiranagar", "Koramangala", "HSR", ...]
}
```

---

## 3. Get Recommendations
`POST /api/v1/recommendations`

Executes the full AI recommendation pipeline.

**Request Body:**
```json
{
  "location": "Indiranagar",
  "budget": "medium",
  "cuisine": "Italian, Chinese",
  "minimum_rating": 3.5,
  "additional_preferences": "romantic, outdoor seating",
  "top_k": 5,
  "llm_model": "llama-3.1-8b-instant"
}
```

**Response:**
```json
{
  "generated_at_utc": "2026-05-01T08:30:00Z",
  "total_results": 5,
  "recommendations": [
    {
      "restaurant_name": "Toscano",
      "cuisine": "Italian",
      "estimated_cost_for_two": 1500,
      "rating": 4.5,
      "ai_explanation": "Perfect for a romantic evening with authentic Italian flavors...",
      "rank": 1,
      "location": "Indiranagar"
    }
  ],
  "meta": {
    "response_time_ms": 1250,
    "llm_model": "llama-3.1-8b-instant"
  }
}
```
