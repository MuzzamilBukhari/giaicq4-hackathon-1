# Railway to Render Migration Guide

This document explains the migration from Railway to Render for the RAG chatbot backend.

## What Changed

### Files Removed
- ✅ `railway.toml` - Railway-specific configuration file

### Files Added
- ✅ `render.yaml` - Render Blueprint configuration (Infrastructure as Code)

### Files Modified
- ✅ `Dockerfile` - Updated CMD to use `$PORT` environment variable
- ✅ `.env.example` - Added `PYTHON_VERSION` for Render
- ✅ `DEPLOYMENT.md` - Complete rewrite for Render deployment
- ✅ `README.md` - Updated deployment section

### Key Differences: Railway vs Render

| Aspect | Railway | Render |
|--------|---------|--------|
| **Config File** | `railway.toml` | `render.yaml` |
| **Port Handling** | `$PORT` env var | `$PORT` env var |
| **Root Directory** | Auto-detected | Must specify for monorepo |
| **Health Check** | Optional | Recommended (`/status`) |
| **Free Tier** | 500 hrs/month | 750 hrs/month, auto-suspend |
| **CLI Tool** | `@railway/cli` | Not needed (dashboard only) |
| **Auto-Deploy** | On git push | On git push |
| **Build Command** | Auto or custom | Custom required |
| **Start Command** | Auto or custom | Custom required |

## Migration Steps

### 1. Update Your Repository

```bash
cd backend
git pull origin 001-rag-chatbot  # Get latest changes
```

The following files have been updated for Render:
- `render.yaml` (new)
- `Dockerfile` (updated)
- `.env.example` (updated)
- `DEPLOYMENT.md` (rewritten)
- `README.md` (updated)

### 2. Deploy to Render

Choose one of two methods:

#### Method A: Blueprint Deployment (Recommended)

1. Commit and push changes (if not already done):
   ```bash
   git add .
   git commit -m "Migrate from Railway to Render"
   git push origin 001-rag-chatbot
   ```

2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Blueprint"
4. Connect GitHub repository
5. Select branch: `001-rag-chatbot`
6. Render will detect `render.yaml`
7. Set required environment variables:
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `NEON_DB_URL`
   - `OPENAI_API_KEY`
8. Click "Apply"

#### Method B: Manual Dashboard Deployment

See `DEPLOYMENT.md` for detailed manual deployment instructions.

### 3. Configure Environment Variables

Set the same environment variables you used in Railway:

| Variable | Example Value |
|----------|---------------|
| `QDRANT_URL` | `https://xxxxx.us-east.aws.cloud.qdrant.io` |
| `QDRANT_API_KEY` | `your-api-key` |
| `QDRANT_COLLECTION_NAME` | `textbook_chunks` |
| `NEON_DB_URL` | `postgresql://user:pass@host.neon.tech/db?sslmode=require` |
| `OPENAI_API_KEY` | `sk-proj-...` |
| `ALLOWED_ORIGINS` | `http://localhost:3000,https://yourdomain.com` |
| `PYTHON_VERSION` | `3.11.0` |

### 4. Verify Deployment

```bash
# Check health
curl https://your-app.onrender.com/status

# Test query
curl -X POST https://your-app.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ROS 2?", "mode": "full_retrieval"}'
```

### 5. Update Frontend Configuration

If you have a frontend connecting to the backend:

1. Update the API base URL:
   ```javascript
   // Before (Railway)
   const API_URL = 'https://your-app.railway.app';
   
   // After (Render)
   const API_URL = 'https://your-app.onrender.com';
   ```

2. Update CORS origins in Render:
   - Add your frontend domain to `ALLOWED_ORIGINS`

### 6. Re-index Documents (If Needed)

If you're using different Qdrant/Neon instances:

```bash
cd backend
python index_docs.py --docs-path ../docusaurus-project/docs --chunk-size 600 --overlap 80
```

## Advantages of Render

### Why We Switched

1. **Better Free Tier**: 750 hours/month vs Railway's 500 hours
2. **Infrastructure as Code**: `render.yaml` for reproducible deployments
3. **Better Documentation**: More comprehensive guides for Python/FastAPI
4. **Predictable Pricing**: Clear upgrade path from free → $7/month → $25/month
5. **Health Checks**: Built-in health monitoring
6. **Zero Config Suspending**: Free tier auto-suspends after 15min (saves resources)

### Trade-offs

1. **Cold Starts**: Free tier spins down after inactivity (30s to wake up)
2. **No CLI**: Must use dashboard (but `render.yaml` compensates)
3. **Monorepo Setup**: Must explicitly set root directory to `backend`

## Rollback Plan

If you need to rollback to Railway:

1. Restore `railway.toml`:
   ```bash
   git revert <commit-hash>
   ```

2. Update Dockerfile CMD:
   ```dockerfile
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. Redeploy to Railway

## Common Issues & Solutions

### Issue: Build Fails on Render

**Cause**: Requirements not installing

**Solution**: 
```bash
# Test locally first
pip install -r requirements.txt
```

Check Python version matches:
- Render: `PYTHON_VERSION=3.11.0`
- Local: `python --version`

### Issue: Health Check Failing

**Cause**: Service not responding on `/status`

**Solution**: Check logs for startup errors
```
Dashboard → Your Service → Logs
```

### Issue: Slow First Request

**Cause**: Free tier cold start

**Solution**: 
- Accept 30s first request (free tier)
- Upgrade to Starter plan ($7/month) for always-on
- Use external monitor to ping every 10min

## Support

- **Render Docs**: https://render.com/docs
- **Render Support**: support@render.com
- **Community**: https://community.render.com

## Next Steps

1. ✅ Migrate to Render
2. ✅ Verify deployment
3. ⬜ Update frontend API URL
4. ⬜ Test end-to-end functionality
5. ⬜ Monitor performance
6. ⬜ Consider upgrading to paid plan for production
