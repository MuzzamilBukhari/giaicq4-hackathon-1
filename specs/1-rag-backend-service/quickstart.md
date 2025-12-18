# Quickstart Guide: RAG Backend Service

**Feature**: 1-rag-backend-service
**Created**: 2025-12-17

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Access to Qdrant Cloud instance
- Google Gemini API key
- Git for version control

## Environment Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd rag-backend-service
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn qdrant-client openai python-dotenv sse-starlette
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:

```env
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-1.5-pro
QDRANT_COLLECTION_NAME=book_content
CORS_ORIGINS=["http://localhost:3000", "https://your-docusaurus-site.com"]
```

## Development Server

### 1. Run Local Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Verify Installation
- Visit `http://localhost:8000/health` to check service status
- Visit `http://localhost:8000/docs` for interactive API documentation

## Testing

### 1. Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this book about?"}'
```

### 2. Test Health Check
```bash
curl http://localhost:8000/health
```

## Production Deployment

### 1. Build Configuration
- Set environment variables for production
- Configure reverse proxy (nginx recommended)
- Set up process manager (gunicorn for multi-worker)

### 2. Run Production Server
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Configuration Options

### Qdrant Settings
- `QDRANT_COLLECTION_NAME`: Name of the collection containing book embeddings
- `QDRANT_SEARCH_LIMIT`: Number of results to retrieve (default: 5)
- `QDRANT_SCORE_THRESHOLD`: Minimum relevance score (default: 0.3)

### Gemini Settings
- `GEMINI_MODEL`: Model to use (default: gemini-1.5-pro)
- `GEMINI_TEMPERATURE`: Response randomness (default: 0.7)

### CORS Settings
- `CORS_ORIGINS`: List of allowed origins for cross-origin requests
- `CORS_ALLOW_CREDENTIALS`: Whether to allow credentials (default: false)

## Troubleshooting

### Common Issues
1. **Qdrant Connection**: Verify URL and API key are correct
2. **Gemini API**: Check Google API key and billing setup
3. **CORS Errors**: Ensure frontend domain is in CORS_ORIGINS

### Logging
- Set `LOG_LEVEL` environment variable (debug, info, warning, error)
- Check application logs for detailed error information