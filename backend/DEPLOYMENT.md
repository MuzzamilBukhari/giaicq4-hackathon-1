# Render Deployment Guide

This guide covers deploying the FastAPI RAG chatbot backend to Render.com.

## Prerequisites

Before deploying to Render, make sure you have:

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Environment Variables Ready**:
   - Qdrant Cloud URL and API Key
   - Neon Postgres Database URL
   - OpenAI API Key

## Step 1: Prepare External Services

### Qdrant Cloud Setup
1. Go to [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a free cluster (1GB included in free tier)
3. Note your cluster URL (format: `https://xxxxx.us-east.aws.cloud.qdrant.io`)
4. Copy your API key from the cluster settings
5. The collection will be created automatically on first run

### Neon Postgres Setup
1. Go to [neon.tech](https://neon.tech)
2. Create a new project (Free tier: 0.5GB storage)
3. Copy the connection string (should include `?sslmode=require`)
4. Format: `postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require`
5. Database tables will be created automatically on first run

### OpenAI API Key
1. Get your API key from [platform.openai.com](https://platform.openai.com/api-keys)
2. Make sure you have credits available
3. Format: `sk-proj-...` or `sk-...`

## Step 2: Deploy to Render

### Option A: Deploy with render.yaml (Infrastructure as Code - Recommended)

1. **Push render.yaml to GitHub**
   
   The `render.yaml` file is located in the **repository root** (not in `/backend`). This file tells Render to:
   - Use the `backend` directory as the root directory for the service
   - Install dependencies from `backend/requirements.txt`
   - Run the FastAPI app from `backend/app/main.py`
   
   ```bash
   git add render.yaml
   git commit -m "Add Render deployment configuration"
   git push origin 001-rag-chatbot
   ```

2. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository and branch: `001-rag-chatbot`
   - Render will auto-detect `render.yaml`

3. **Set Environment Variables**
   Before deploying, you'll be prompted to set these secret variables:
   ```
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   NEON_DB_URL=postgresql://username:password@your-neon-host.neon.tech/dbname?sslmode=require
   OPENAI_API_KEY=sk-your-openai-api-key
   ```

4. **Apply Blueprint**
   - Review the configuration
   - Click "Apply" to create and deploy the service

### Option B: Manual Deployment (Dashboard)

### Option B: Manual Deployment (Dashboard)

1. **Create New Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository and branch: `001-rag-chatbot`

2. **Configure Service Settings**
   - **Name**: `rag-chatbot-api` (or your preferred name)
   - **Region**: Oregon (US West) or Frankfurt (EU) - choose closest to users
   - **Branch**: `001-rag-chatbot`
   - **Root Directory**: `backend` *(important for monorepo)*
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   Go to "Environment" tab and add:
   
   | Key | Value | Secret |
   |-----|-------|--------|
   | `PYTHON_VERSION` | `3.11.0` | No |
   | `QDRANT_URL` | `https://your-cluster.qdrant.io` | Yes |
   | `QDRANT_API_KEY` | `your-qdrant-api-key` | Yes |
   | `QDRANT_COLLECTION_NAME` | `textbook_chunks` | No |
   | `NEON_DB_URL` | `postgresql://...` | Yes |
   | `OPENAI_API_KEY` | `sk-...` | Yes |
   | `ALLOWED_ORIGINS` | `http://localhost:3000,https://yourdomain.com` | No |
   | `APP_NAME` | `RAG Chatbot` | No |
   | `DEBUG` | `False` | No |

4. **Configure Advanced Settings**
   - **Health Check Path**: `/status`
   - **Auto-Deploy**: Yes (recommended)
   - **Instance Type**: Free (or upgrade for production)

5. **Create Web Service**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - You'll get a public URL like `https://rag-chatbot-api.onrender.com`

## Step 3: Verify Deployment

1. **Check Health Status**
   ```bash
   curl https://your-app.onrender.com/status
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
   curl -X POST https://your-app.onrender.com/query \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is ROS 2?",
       "mode": "full_retrieval"
     }'
   ```

## Step 4: Index Your Documents

Before the chatbot can answer questions, you need to index your documents.

### Local Indexing (Recommended)

Run the indexer script from your local machine:

```bash
cd backend

# Set environment variables (create .env file with your production credentials)
cp .env.example .env
# Edit .env with your Qdrant, Neon, and OpenAI credentials

# Run indexer
python index_docs.py --docs-path ../docusaurus-project/docs --chunk-size 600 --overlap 80
```

This will:
- Parse all Markdown files from your docs directory
- Split them into 600-token chunks with 80-token overlap
- Generate embeddings using OpenAI
- Store vectors in Qdrant and metadata in Neon

### Monitor Indexing Progress

Watch the console output for:
- Number of files processed
- Total chunks created
- Any errors or warnings

## Step 5: Update CORS Origins

Once you have your Render URL, update the `ALLOWED_ORIGINS` environment variable:

1. Go to Render Dashboard → Your Service → Environment
2. Edit `ALLOWED_ORIGINS`:
   ```
   http://localhost:3000,https://your-app.onrender.com,https://your-docusaurus-site.vercel.app
   ```
3. Save changes (service will auto-redeploy)

## Monitoring and Maintenance

### View Logs
- Render Dashboard → Your Service → Logs
- Real-time log streaming
- Search and filter capabilities

### Check Performance Metrics
```bash
curl https://your-app.onrender.com/metrics
```

Response includes:
- Average latency (ms)
- Success rate (%)
- Request counts
- Percentile latencies (p50, p95, p99)

### Service Management
- **Manual Deploy**: Click "Manual Deploy" → "Deploy latest commit"
- **Restart**: Click "Manual Deploy" → "Clear build cache & deploy"
- **Suspend**: Free tier services auto-suspend after 15min inactivity
- **Spin Up**: First request after suspension takes ~30 seconds

## Troubleshooting

### Build Fails

**Issue**: Dependencies fail to install
- Check `requirements.txt` is valid
- Verify Python version is 3.11
- Check Render build logs for specific errors

**Solution**:
```bash
# Test locally first
pip install -r requirements.txt
```

### Connection Errors

**Issue**: Cannot connect to Qdrant or Neon
- Verify URLs are correct (no trailing slashes)
- Verify API keys are valid
- Check Neon connection string includes `?sslmode=require`

**Solution**: Check Render environment variables and logs:
```
Dashboard → Environment → Verify all secrets are set
Dashboard → Logs → Search for connection errors
```

### Service Won't Start

**Issue**: Service fails health check
- Health check endpoint `/status` not responding
- Port configuration mismatch

**Solution**: Verify start command uses `$PORT`:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Rate Limiting

**Issue**: Getting 429 errors
- Default: 10 requests per minute per IP
- Too restrictive for your use case

**Solution**: Adjust in `app/rate_limiter.py`:
```python
rate_limiter = RateLimiter(max_requests=30, window_size=60)
```

### CORS Errors

**Issue**: Frontend can't access API
- CORS policy blocking requests

**Solution**: Add frontend domain to `ALLOWED_ORIGINS`:
```
https://your-frontend.vercel.app,https://www.yourdomain.com
```

### Slow Cold Starts (Free Tier)

**Issue**: First request takes 30+ seconds
- Free tier spins down after 15min inactivity
- Render needs to wake up the service

**Solutions**:
1. Upgrade to paid plan (keeps service alive 24/7)
2. Use external uptime monitor (pings every 10min)
3. Accept cold starts for low-traffic applications

## Cost Considerations

### Render Pricing
- **Free Tier**: 
  - 750 hours/month
  - Spins down after 15min inactivity
  - Shared CPU/RAM
  - Good for development/testing

- **Starter ($7/month)**:
  - Always-on service
  - 512MB RAM
  - 0.5 CPU
  - Good for production

### External Services
- **Qdrant Cloud**: Free tier includes 1GB cluster
- **Neon**: Free tier includes 0.5GB storage  
- **OpenAI**: Pay-per-use
  - Embeddings: ~$0.0001/1K tokens
  - GPT-4o: ~$0.005/1K input tokens, ~$0.015/1K output tokens

### Estimated Monthly Costs
- **Development**: $0 (all free tiers)
- **Light Production**: $7 (Render Starter) + ~$5 (OpenAI) = $12/month
- **Medium Production**: $25 (Render Pro) + ~$20 (OpenAI) = $45/month

## Auto-Deploy on Git Push

Render automatically deploys when you push to your connected branch:

```bash
git add .
git commit -m "Update RAG backend"
git push origin 001-rag-chatbot
```

Render will:
1. Detect the push
2. Run build command
3. Run health checks
4. Deploy new version
5. Notify you via email/Slack (if configured)

## Environment-Specific Deployments

### Development Environment
- Branch: `dev` or `001-rag-chatbot`
- Service name: `rag-chatbot-dev`
- Separate database and vector store

### Production Environment  
- Branch: `main`
- Service name: `rag-chatbot-prod`
- Production credentials
- Paid plan for reliability

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Index your textbook content
3. ⬜ Integrate chatbot widget into Docusaurus frontend
4. ⬜ Test end-to-end functionality
5. ⬜ Set up monitoring and alerts
6. ⬜ Configure custom domain (optional)

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-fastapi)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Neon Documentation](https://neon.tech/docs/introduction)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
