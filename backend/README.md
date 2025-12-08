# RAG Chatbot Backend

This is the backend service for the RAG (Retrieval-Augmented Generation) Chatbot system that provides AI-powered answers to questions about textbook content.

## Features

- **FastAPI-based API**: Provides endpoints for querying textbook content
- **Qdrant Vector Database**: Stores document embeddings for semantic search
- **Neon Postgres**: Stores document metadata and provenance information
- **OpenAI Integration**: Uses ChatKit for answer generation with citations
- **Rate Limiting**: Prevents abuse with per-IP rate limiting
- **Performance Monitoring**: Tracks latency and success rates
- **Docusaurus Integration**: Frontend widget for textbook sites

## Endpoints

- `POST /query`: Query textbook content with retrieval-augmented generation
- `POST /selected`: Query using selected text only (no vector lookup)
- `GET /status`: Health check endpoint
- `GET /metrics`: Performance metrics endpoint

## Environment Variables

- `QDRANT_URL`: URL to your Qdrant Cloud cluster
- `QDRANT_API_KEY`: API key for Qdrant authentication
- `NEON_DB_URL`: Full connection string for Neon Postgres
- `OPENAI_API_KEY`: OpenAI API key for embeddings and generation
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS (default: "http://localhost:3000,http://localhost:3001,https://yourdomain.com")

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:
   ```bash
   QDRANT_URL=your-qdrant-url
   QDRANT_API_KEY=your-api-key
   NEON_DB_URL=your-neon-connection-string
   OPENAI_API_KEY=your-openai-api-key
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## Indexing Documents

To index documents from the `/docs/` directory:

```bash
python scripts/index_docs.py --docs-path ../docs --chunk-size 600 --overlap 80
```

## Running Tests

```bash
pytest tests/
```

## Deployment

The service is designed for deployment on Render.com. See `DEPLOYMENT.md` for detailed deployment instructions including:
- Setting up Qdrant Cloud and Neon Postgres
- Configuring environment variables
- Deploying with render.yaml or manually via dashboard
- Indexing documents
- Monitoring and troubleshooting

## Architecture

The system follows a microservice architecture with the following components:

- **API Gateway**: FastAPI application handling HTTP requests
- **Embedder**: Converts text to vector embeddings using OpenAI's API
- **Vector Database**: Qdrant Cloud stores document chunks as vectors
- **Metadata Store**: Neon Postgres stores document metadata
- **AI Agent**: Uses OpenAI for answer generation with proper citations