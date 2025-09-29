# API Spec (Preview)

## Classification Endpoint
POST /api/classify
Body: { "features": { ... } }
Response: { "family": "...", "level": "...", "probs": { ... } }

## Health
GET /api/health
Response: { "status": "ok" }
