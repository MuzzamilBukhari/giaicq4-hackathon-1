# RAG Chatbot Backend

This is the backend service for the RAG (Retrieval-Augmented Generation) Chatbot system for the Physical AI & Humanoid Robotics textbook. It uses Cohere for embeddings and answer generation.

## Features

- Global Q&A over the entire textbook content
- Local Q&A restricted to specific text selections
- Citation system returning source metadata and URLs
- Session management with conversation history
- Integration with Qdrant vector database and Neon Postgres
- Authentication-free operation for immediate use
- Grounded responses based solely on textbook content

## Tech Stack

- FastAPI: Web framework
- Cohere: Embeddings and text generation
- Qdrant: Vector database for document chunks
- Neon Postgres: Session and user data storage
- SQLAlchemy: Database ORM
- Alembic: Database migrations

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the required values:
   ```bash
   cp .env.example .env
   ```
4. Set up your environment variables:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant Cloud URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `DATABASE_URL`: Your Neon Postgres connection string

## Running the Backend

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### RAG Endpoints
- `POST /api/ask`: Global Q&A with retrieval from textbook
- `POST /api/ask-selected`: Q&A based only on selected text
- `GET /api/history/{session_id}`: Get conversation history

## Ingestion

To ingest textbook content into the vector database:

1. Place your markdown files in a `docs/` directory
2. Run the ingestion script:
   ```bash
   python ingest.py
   ```

This will chunk the documents, generate embeddings using Cohere, and upload them to Qdrant.

## Deployment to Hugging Face

This backend is designed to run on Hugging Face Spaces/Inference API:

1. Create a new Space with CPU Basic tier
2. Add your environment variables in the Space settings
3. The application will automatically start using the `main.py` file

## Database Migrations

Run database migrations using Alembic:

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head
```

## Environment Variables

- `COHERE_API_KEY`: Cohere API key (required)
- `QDRANT_URL`: Qdrant Cloud URL (required)
- `QDRANT_API_KEY`: Qdrant API key (required)
- `QDRANT_COLLECTION`: Name of the Qdrant collection (default: book_chunks)
- `DATABASE_URL`: Postgres database connection string (required)
