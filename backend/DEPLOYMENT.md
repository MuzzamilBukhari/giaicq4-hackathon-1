# Railway Deployment Guide

## Prerequisites

Before deploying to Railway, make sure you have:

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Environment Variables Ready**:
   - Qdrant Cloud URL and API Key
   - Neon Postgres Database URL
   - OpenAI API Key

## Step 1: Prepare External Services

### Qdrant Cloud Setup
1. Go to [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a free cluster
3. Note your cluster URL and API key
4. The collection will be created automatically on first run

### Neon Postgres Setup
1. Go to [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string (should include `?sslmode=require`)
4. Database tables will be created automatically on first run

### OpenAI API Key
1. Get your API key from [platform.openai.com](https://platform.openai.com/api-keys)
2. Make sure you have credits available

## Step 2: Deploy to Railway

### Option A: Deploy from GitHub (Recommended)

1. **Connect GitHub Repository**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the `001-rag-chatbot` branch

2. **Configure Service**
   - Railway will detect the Dockerfile automatically
   - Set the root directory to `/backend` if needed

3. **Set Environment Variables**
   Click on "Variables" and add:
   ```
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   QDRANT_COLLECTION_NAME=textbook_chunks
   NEON_DB_URL=postgresql://username:password@your-neon-host.neon.tech/dbname?sslmode=require
   OPENAI_API_KEY=sk-your-openai-api-key
   ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
   ```

4. **Deploy**
   - Railway will automatically build and deploy
   - You'll get a public URL like `https://your-app.railway.app`

### Option B: Deploy with Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   cd backend
   railway init
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set QDRANT_URL=https://your-cluster.qdrant.io
   railway variables set QDRANT_API_KEY=your-qdrant-api-key
   railway variables set NEON_DB_URL=postgresql://...
   railway variables set OPENAI_API_KEY=sk-...
   railway variables set ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
   ```

5. **Deploy**
   ```bash
   railway up
   ```

## Step 3: Verify Deployment

1. **Check Health Status**
   ```bash
   curl https://your-app.railway.app/status
   ```

   Expected response:
   ```json
   {
     "status": "healthy",
     "app_version": "1.0.0",
     "qdrant_ok": true,
     "neon_ok": true,
     "vector_count": 0
   }
   ```

2. **Test Query Endpoint**
   ```bash
   curl -X POST https://your-app.railway.app/query \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is ROS 2?",
       "mode": "full_retrieval"
     }'
   ```

## Step 4: Index Your Documents

Before the chatbot can answer questions, you need to index your documents:

1. **Run the indexer script** (locally or from a separate worker):
   ```bash
   python scripts/index_docs.py --docs-path ../docusaurus-project/docs --chunk-size 600 --overlap 80
   ```

2. This will:
   - Parse all Markdown files
   - Split them into chunks
   - Generate embeddings
   - Store in Qdrant and Neon

## Step 5: Update CORS Origins

Once you have your Railway URL, update the `ALLOWED_ORIGINS` environment variable:

```
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.railway.app,https://your-docusaurus-site.vercel.app
```

## Monitoring

### View Logs
- Railway Dashboard → Your Service → Logs
- Or use CLI: `railway logs`

### Check Metrics
```bash
curl https://your-app.railway.app/metrics
```

Response includes:
- Average latency
- Success rate
- Request counts
- Percentile latencies (p50, p95, p99)

## Troubleshooting

### Build Fails
- Check that `railway.toml` and `Dockerfile` are in the `/backend` directory
- Verify requirements.txt has all dependencies

### Connection Errors
- Verify Qdrant URL and API key
- Verify Neon connection string includes `?sslmode=require`
- Check Railway logs for specific error messages

### Rate Limiting
- Default: 10 requests per minute per IP
- Adjust in `app/rate_limiter.py` if needed

### CORS Errors
- Add your frontend domain to `ALLOWED_ORIGINS`
- Separate multiple origins with commas

## Cost Considerations

- **Railway**: Free tier includes 500 hours/month
- **Qdrant Cloud**: Free tier includes 1GB cluster
- **Neon**: Free tier includes 0.5GB storage
- **OpenAI**: Pay-per-use (embeddings + completions)

Estimated monthly cost for moderate usage: $5-20

## Next Steps

1. ✅ Deploy backend to Railway
2. ⬜ Index your textbook content
3. ⬜ Integrate chatbot widget into Docusaurus frontend
4. ⬜ Test end-to-end functionality
5. ⬜ Monitor performance and costs
