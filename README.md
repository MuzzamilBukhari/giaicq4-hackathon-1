# RAG Backend Service for Deployed Book

A standalone backend service that powers the RAG chatbot for the deployed Docusaurus book.

## Overview

This service provides a FastAPI-based backend that:
- Accepts user queries via HTTP endpoints
- Retrieves relevant context from Qdrant Cloud instance
- Processes queries with Google Gemini via OpenAI-compatible endpoint
- Returns responses compatible with the Docusaurus RAG widget

## Project Structure

```
rag-backend-service/
├── src/                    # Source code
│   ├── api/               # FastAPI endpoints
│   ├── db/                # Database connections
│   ├── llm/               # LLM integration
│   ├── models/            # Data models
│   ├── retrieval/         # Context retrieval logic
│   ├── services/          # Business logic
│   ├── utils/             # Utility functions
│   └── middleware/        # Middleware components
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Start development server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## API Endpoints

- `POST /chat` - Process user queries with RAG capabilities
- `GET /health` - Service health check

## Environment Variables

- `QDRANT_URL` - Qdrant Cloud cluster URL
- `QDRANT_API_KEY` - Qdrant API key
- `QDRANT_COLLECTION_NAME` - Name of the collection containing book embeddings
- `GOOGLE_API_KEY` - Google API key for Gemini
- `GEMINI_MODEL` - Name of the Gemini model to use
- `GEMINI_BASE_URL` - OpenAI-compatible endpoint for Gemini
- `CORS_ORIGINS` - List of allowed origins for CORS
- `LOG_LEVEL` - Logging level (default: info)