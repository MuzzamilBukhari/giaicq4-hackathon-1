# RAG Chatbot Architecture

## Overview

The RAG (Retrieval-Augmented Generation) Chatbot system provides students and readers with an AI-powered assistant that can answer questions about textbook content. The system uses a combination of vector search and language model generation to provide accurate, cited answers.

## System Components

### Backend Services

The backend is built with FastAPI and consists of several key components:

- **API Gateway**: FastAPI application handling HTTP requests
- **Embedder**: Converts text to vector embeddings using OpenAI's text-embedding-3-small model
- **Vector Database**: Qdrant Cloud stores document chunks as vectors for semantic search
- **Metadata Store**: Neon Postgres stores document metadata and provenance information
- **AI Agent**: Uses OpenAI ChatKit for answer generation with proper citations

### Frontend Widget

The Docusaurus chat widget provides a seamless interface for users:

- **Modal Interface**: Opens as an overlay on any textbook page
- **Text Selection**: Detects and uses highlighted text for queries
- **Response Display**: Shows answers with source citations and links

## Data Flow

### Indexing Process

1. Markdown files from `/docs/` are parsed and chunked
2. Chunks are converted to vector embeddings
3. Vectors are stored in Qdrant with metadata
4. Metadata is stored in Neon Postgres for provenance

### Query Process

1. User submits a question via the chat widget
2. Question is converted to a vector embedding
3. Vector search retrieves relevant document chunks
4. AI agent generates answer with citations
5. Response is returned to the frontend

## Technology Stack

- **Backend**: Python 3.11, FastAPI
- **Vector Database**: Qdrant Cloud
- **Metadata Store**: Neon Postgres
- **AI Models**: OpenAI GPT-4o and text-embedding-3-small
- **Frontend**: React component integrated with Docusaurus
- **Deployment**: Railway.app

## Security

- API keys are stored as environment variables
- CORS is configured to allow only specified origins
- Rate limiting prevents abuse
- No sensitive information is stored in the frontend