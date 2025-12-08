# Deployment Guide

This guide will walk you through deploying the RAG Chatbot system to Railway and testing it with your textbook content.

## Prerequisites

Before you begin, you'll need accounts for the following services:

1. **Railway**: [https://railway.app](https://railway.app) - for backend hosting
2. **Qdrant Cloud**: [https://qdrant.tech](https://qdrant.tech) - for vector database
3. **Neon**: [https://neon.tech](https://neon.tech) - for metadata storage
4. **OpenAI**: [https://platform.openai.com](https://platform.openai.com) - for embeddings and generation

## Step 1: Set up External Services

### Qdrant Cloud Setup
1. Create an account at [qdrant.tech](https://qdrant.tech)
2. Create a new cluster
3. Note your cluster URL and API key
4. The system will automatically create the required collection

### Neon Setup
1. Create an account at [neon.tech](https://neon.tech)
2. Create a new project
3. Note your connection string (looks like: `postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname`)
4. The system will automatically create required tables

### OpenAI Setup
1. Create an account at [platform.openai.com](https://platform.openai.com)
2. Create an API key in the dashboard
3. Note your API key

## Step 2: Deploy to Railway

### Option A: Using GitHub Integration (Recommended)
1. Push your code to a GitHub repository
2. Go to [railway.app](https://railway.app) and sign in
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect the `railway.toml` configuration

### Option B: Using Railway CLI
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Navigate to the `backend` directory: `cd backend`
4. Link to a new project: `railway init`
5. Deploy: `railway up`

## Step 3: Configure Environment Variables

After deployment, set these environment variables in Railway:

1. Go to your Railway project dashboard
2. Click on "Variables"
3. Add these variables:

```
QDRANT_URL=your-qdrant-cluster-url
QDRANT_API_KEY=your-qdrant-api-key
NEON_DB_URL=your-neon-connection-string
OPENAI_API_KEY=your-openai-api-key
ALLOWED_ORIGINS=https://yourdomain.com,http://localhost:3000
```

## Step 4: Test the Backend

### Verify Deployment
1. Visit your Railway project URL
2. Test the status endpoint: `GET /status`
3. You should see a response like:
```json
{
  "status": "healthy",
  "app_version": "1.0.0",
  "qdrant_ok": true,
  "neon_ok": true,
  "vector_count": 0,
  "performance_metrics": {...}
}
```

### Test API Endpoints
1. Test the query endpoint:
```bash
curl -X POST https://your-app.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this textbook about?"
  }'
```

## Step 5: Index Your Textbook Content

### Prepare Your Content
1. Make sure your textbook content is in the `/docs/` directory in markdown format
2. Ensure all files have proper headings and structure

### Run the Indexer
1. SSH into your Railway deployment or run locally with the same environment variables
2. Run the indexing script:

```bash
cd backend
python scripts/index_docs.py --docs-path /path/to/your/docs --chunk-size 600 --overlap 80
```

### Verify Indexing
1. Check the vector count: `python scripts/qdrant_manage.py --count`
2. You should see a number greater than 0 if documents were indexed successfully

## Step 6: End-to-End Testing

### Test Queries
1. Test with a question about your content:
```bash
curl -X POST https://your-app.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key concepts in Chapter 1?"
  }'
```

2. Test the selected text feature:
```bash
curl -X POST https://your-app.railway.app/selected \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain this concept",
    "selected_text": "Your selected text here..."
  }'
```

### Check Performance
1. Monitor the metrics: `GET /metrics`
2. Look for reasonable latency (under 5 seconds) and high success rate

## Step 7: Integrate with Docusaurus

### Update Frontend Configuration
1. In your Docusaurus project, update the RAGChatWidget to point to your deployed backend:

```js
<RAGChatWidget
  backendUrl="https://your-app.railway.app"  // Replace with your Railway URL
  allowedOrigins={["https://yourdomain.com"]}  // Replace with your domain
/>
```

### Build and Deploy Docusaurus
1. Build your Docusaurus site: `npm run build`
2. Deploy to your hosting platform (Vercel, Netlify, GitHub Pages, etc.)

## Step 8: Validation and Testing

### Automated Testing

The repository includes testing scripts to help validate your deployment:

1. **Test Deployment Script**:
   ```bash
   python scripts/test_deployment.py --base-url https://your-app.railway.app
   ```

2. **Validate Deployment Script**:
   ```bash
   python scripts/validate_deployment.py --base-url https://your-app.railway.app
   ```

### Manual Validation Checklist

Before going live, verify:

- [ ] Backend API is accessible and healthy
- [ ] Documents are properly indexed (check vector count > 0)
- [ ] Queries return relevant answers with citations
- [ ] Selected text feature works correctly
- [ ] Rate limiting is functioning
- [ ] CORS is properly configured
- [ ] Frontend widget appears on all pages
- [ ] Performance metrics are acceptable (responses under 5s)
- [ ] Error handling works appropriately

## Troubleshooting

### Common Issues
1. **Connection errors**: Verify all API keys and connection strings are correct
2. **Empty results**: Ensure documents were properly indexed
3. **Slow queries**: Check your Qdrant cluster performance tier
4. **CORS errors**: Verify ALLOWED_ORIGINS includes your frontend domain

### Monitoring
- Check Railway logs for errors: `railway logs`
- Monitor the `/status` and `/metrics` endpoints
- Use the `/health` endpoint to verify all dependencies

## Next Steps

Once deployment and testing are successful:
1. Set up automatic deployment from your GitHub repository
2. Configure monitoring and alerting
3. Plan for scaling based on expected usage
4. Set up backup procedures for your databases