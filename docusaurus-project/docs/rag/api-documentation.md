# API Documentation

## Overview

The RAG Chatbot API provides endpoints for querying textbook content using retrieval-augmented generation. All endpoints return JSON responses and use standard HTTP status codes.

## Base URL

The API is deployed at: `https://your-rag-backend.railway.app`

## Authentication

The API does not require authentication for basic operations. Rate limiting is applied per IP address.

## Endpoints

### POST /query

Query textbook content with retrieval-augmented generation.

#### Request

```json
{
  "question": "What is forward kinematics?",
  "mode": "full_retrieval",
  "selected_text": "Optional text to use instead of vector search"
}
```

**Parameters:**
- `question` (string, required): The question to ask about textbook content
- `mode` (string, optional): Query mode - 'full_retrieval' (default) or 'selected_text_only'
- `selected_text` (string, optional): Text to use for 'selected_text_only' mode

#### Response

```json
{
  "answer": "Forward kinematics calculates the end-effector position from joint angles...",
  "sources": [
    {
      "doc_path": "/docs/module-3/kinematics.md",
      "heading": "Forward vs Inverse Kinematics",
      "excerpt": "Forward kinematics is the process of calculating the position...",
      "score": 0.85
    }
  ],
  "meta": {
    "latency_ms": 2450,
    "model": "gpt-4o",
    "retrieval_count": 3
  }
}
```

### POST /selected

Query using selected text only (no vector lookup).

#### Request

```json
{
  "question": "Can you explain this concept?",
  "selected_text": "Forward kinematics is the process of calculating the position and orientation of the end-effector..."
}
```

**Parameters:**
- `question` (string, required): The question about the selected text
- `selected_text` (string, required): The text to use as context

#### Response

Same format as `/query` endpoint.

### GET /status

Health check endpoint that verifies the status of all dependencies.

#### Response

```json
{
  "status": "healthy",
  "app_version": "1.0.0",
  "qdrant_ok": true,
  "neon_ok": true,
  "vector_count": 1500
}
```

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing the issue"
}
```

### Common HTTP Status Codes

- `200`: Success
- `400`: Bad request (invalid parameters)
- `429`: Rate limit exceeded
- `500`: Internal server error

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 10 requests per minute per IP address for query endpoints
- Exceeding the limit returns a 429 status code

## CORS Policy

The API allows requests from configured origins only. By default, this includes the textbook domain and localhost for development.

## Examples

### Query Example

```bash
curl -X POST https://your-rag-backend.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key principles of ROS 2?",
    "mode": "full_retrieval"
  }'
```

### Selected Text Example

```bash
curl -X POST https://your-rag-backend.railway.app/selected \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain this in simpler terms",
    "selected_text": "ROS 2 is a set of libraries and tools that help you build robot applications..."
  }'
```