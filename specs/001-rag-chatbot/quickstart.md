# Quickstart Guide: RAG Chatbot Integration

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Railway account
- Qdrant Cloud account
- Neon Postgres account
- OpenAI API key with ChatKit access

## Local Development Setup

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd hackathon-book
```

### 2. Set Up Backend Environment

```bash
# Navigate to backend directory
mkdir -p backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn qdrant-client psycopg2-binary openai python-dotenv pydantic
```

### 3. Configure Environment Variables

Create a `.env` file in the backend directory:

```env
QDRANT_URL=https://your-qdrant-cluster.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
NEON_DB_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/your-db
OPENAI_API_KEY=your-openai-api-key
CHATKIT_API_KEY=your-chatkit-api-key
RAILWAY_DOMAIN=your-railway-app.railway.app
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 4. Run Local Services

```bash
# Start Qdrant locally with Docker
docker-compose up -d

# Run the FastAPI application
uvicorn app.main:app --reload --port 8000
```

## Running the Indexer

### 1. Index Textbook Content

```bash
# Run the indexing script to process all docs/
python scripts/index_docs.py --docs-path ../docs --chunk-size 600 --overlap 80 --replace

# Run with sample flag for testing
python scripts/index_docs.py --docs-path ../docs --chunk-size 600 --overlap 80 --sample
```

### 2. Verify Indexing

Check that content has been properly chunked and stored:

```bash
# Check vector count in Qdrant
python scripts/qdrant_manage.py --count

# List collections
python scripts/qdrant_manage.py --list
```

## API Usage Examples

### 1. Query Textbook Content

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is forward kinematics?"
  }'
```

### 2. Query with Selected Text Only

```bash
curl -X POST http://localhost:8000/selected \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Can you explain this concept?",
    "selected_text": "Forward kinematics is the process of calculating the position and orientation of the end-effector..."
  }'
```

### 3. Check System Status

```bash
curl http://localhost:8000/status
```

## Docusaurus Integration

### 1. Install the Chat Widget

Add the RAG chat widget to your Docusaurus site by including the React component in your layout:

```jsx
// In your Docusaurus theme or layout
import RAGChatWidget from './components/RAGChatWidget';

// Add to your layout
<RAGChatWidget
  backendUrl="https://your-rag-backend.railway.app"
  allowedOrigins={['https://yourdomain.com']}
/>
```

### 2. Widget Features

- Opens as a modal/panel from any page
- Detects highlighted text via `window.getSelection()`
- Toggle: "Use selected text only"
- Displays answer with source links
- Handles loading, errors, and source expansion

## Deployment to Railway

### 1. Prepare for Deployment

```bash
# Build Docker image
docker build -t rag-chatbot .

# Push to Railway (if using container registry)
# Or connect your GitHub repo to Railway for automatic deployments
```

### 2. Set Environment Variables in Railway

In the Railway dashboard, set the following variables:

```
QDRANT_URL
QDRANT_API_KEY
NEON_DB_URL
OPENAI_API_KEY
CHATKIT_API_KEY
ALLOWED_ORIGINS
```

### 3. Deploy

```bash
# Using Railway CLI
railway up

# Or deploy via GitHub integration
```

## Testing

### 1. Run Unit Tests

```bash
cd backend
python -m pytest tests/unit/
```

### 2. Run Integration Tests

```bash
cd backend
python -m pytest tests/integration/
```

### 3. End-to-End Test

```bash
# Test full query flow
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key concepts in module 1?"
  }'
```

## Troubleshooting

### Common Issues

1. **Connection Errors**: Verify all API keys and URLs are correct
2. **Indexing Failures**: Check that the docs path exists and contains valid markdown
3. **Slow Queries**: Ensure Qdrant collection is properly configured with right vector size
4. **CORS Issues**: Verify ALLOWED_ORIGINS includes your frontend domain

### Health Checks

- `/status` endpoint shows system health
- Check logs in Railway dashboard for errors
- Verify vector count matches expected number of chunks