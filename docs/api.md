# RAG Backend Service API Documentation

## Overview

The RAG Backend Service provides a REST API for interacting with the Retrieval-Augmented Generation system. The API allows users to submit queries about the book content and receive AI-generated responses with relevant citations.

## Base URL

The API is served at the configured base URL. By default, during development it's available at `http://localhost:8000`.

## Authentication

The API does not require authentication for basic functionality. All endpoints are publicly accessible.

## Endpoints

### POST /api/v1/chat

Submit a query to the RAG system and receive a response.

#### Request

```json
{
  "query": "Your question about the book content",
  "session_id": "optional-session-identifier",
  "metadata": {
    "source": "optional metadata object"
  }
}
```

**Request Fields:**

- `query` (string, required): The question or prompt to ask the RAG system. Must be between 1 and 2000 characters.
- `session_id` (string, optional): Identifier for maintaining conversation context.
- `metadata` (object, optional): Additional metadata to include with the request.

#### Response

```json
{
  "id": "unique-response-identifier",
  "answer": "The AI-generated response to your query",
  "sources": [
    {
      "url": "https://example.com/source-url",
      "section": "Section title",
      "relevance_score": 0.85
    }
  ],
  "created_at": "2025-12-17T10:00:00Z",
  "model": "gemini-1.5-pro",
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 200,
    "total_tokens": 350
  }
}
```

**Response Fields:**

- `id` (string): Unique identifier for this response
- `answer` (string): The AI-generated answer to the query
- `sources` (array): List of sources used to generate the response
  - `url` (string): URL of the source document
  - `section` (string): Section title from the source
  - `relevance_score` (number): How relevant this source was (0.0-1.0)
- `created_at` (string): ISO 8601 timestamp of response creation
- `model` (string): Name of the model used
- `usage` (object): Token usage information (optional)

#### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main concept of ROS 2?"
  }'
```

### POST /api/v1/chat/stream

Submit a query to the RAG system and receive a streaming response using Server-Sent Events (SSE).

#### Request

Same request format as `/api/v1/chat`.

#### Response

Server-Sent Events stream with response chunks:

```
data: {"content": "First part of response", "request_id": "unique-id"}

data: {"content": "Second part of response", "request_id": "unique-id"}

data: {"content": "Final part of response", "request_id": "unique-id"}
```

### GET /api/v1/health

Check the health status of the RAG system.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2025-12-17T10:00:00Z",
  "checks": {
    "qdrant_connection": true,
    "gemini_connection": true,
    "api_server": true
  }
}
```

### GET /api/v1/ready

Check if the service is ready to accept traffic.

#### Response

```json
{
  "status": "ready",
  "timestamp": "2025-12-17T10:00:00Z"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid query format or content
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side error during processing
- `503 Service Unavailable`: Service temporarily unavailable

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. By default, the system allows 100 requests per minute per IP address.

## CORS

The API supports Cross-Origin Resource Sharing (CORS) for integration with web frontends. The allowed origins are configured via the `CORS_ORIGINS` environment variable.

## Headers

The API returns several useful headers:

- `X-Request-ID`: Unique identifier for the request, useful for debugging
- `X-Response-Time`: Time taken to process the request (in milliseconds)

## Query Guidelines

- Keep queries between 1 and 2000 characters
- Be specific in your questions for better results
- Questions about the book content will yield the best responses
- The system will cite sources when providing information from the documentation

## Response Quality

The system attempts to provide accurate and helpful responses based on the book content. Responses include citations to relevant sections when available. If the system cannot find relevant information, it will indicate this clearly.