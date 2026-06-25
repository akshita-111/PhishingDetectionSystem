---
title: Phishing Orchestrator Service
emoji: 🛡️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Phishing Orchestrator Service

This service orchestrates phishing detection by coordinating between the brain API (ML model) and providing a unified API endpoint.

## Features

- RESTful API for phishing detection
- Integration with ML-based brain API
- MongoDB for logging detection records
- Health check endpoint
- CORS enabled for cross-origin requests

## API Endpoints

### POST /api/v1/check
Check if a URL is phishing.

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "isPhishing": false,
  "confidence": 0.95,
  "explanation": "URL appears safe"
}
```

### GET /api/v1/health
Health check endpoint.

**Response:**
```json
"Orchestrator service is healthy"
```

## Environment Variables

- `BRAIN_API_URL`: URL of the brain API service (default: https://huggingface.co/spaces/Akshita118/brain-api/predict)
- `MONGODB_URI`: MongoDB connection string (optional, for logging)
- `SERVER_PORT`: Server port (default: 8080)

## Deployment

This service is deployed using Docker. Hugging Face Spaces will automatically build and run the Docker container.

## Usage

Once deployed, you can access the service at:
- Main API: `https://huggingface.co/spaces/Akshita118/phishing-orchestrator/api/v1/check`
- Health check: `https://huggingface.co/spaces/Akshita118/phishing-orchestrator/api/v1/health`
