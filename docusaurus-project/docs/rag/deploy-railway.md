# Deploy to Railway

This guide explains how to deploy the RAG Chatbot backend to Railway.app.

## Prerequisites

- Railway account
- Qdrant Cloud account and API key
- Neon Postgres account and connection string
- OpenAI API key

## Deployment Steps

### 1. Fork and Connect Repository

1. Fork this repository to your GitHub account
2. In Railway, click "New Project"
3. Select "GitHub" and connect your account
4. Choose your forked repository

### 2. Configure Environment Variables

Add the following environment variables in the Railway dashboard:

```
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
NEON_DB_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
OPENAI_API_KEY=your-openai-api-key
CHATKIT_API_KEY=your-chatkit-api-key (if using ChatKit directly)
ALLOWED_ORIGINS=https://yourdomain.com,http://localhost:3000
```

### 3. Set Up the Service

1. Railway should automatically detect the Dockerfile in the backend directory
2. Make sure the working directory is set to `/app/backend`
3. Expose port 8000

### 4. Deploy

1. Click "Deploy Now" in the Railway dashboard
2. Monitor the deployment logs for any errors
3. Once deployed, note the Railway domain URL

### 5. Verify Deployment

1. Visit `https://your-app.railway.app/status` to check system health
2. Test the API endpoints to ensure they're working properly

## Environment Configuration

### Required Variables

- `QDRANT_URL`: URL to your Qdrant Cloud cluster
- `QDRANT_API_KEY`: API key for Qdrant authentication
- `NEON_DB_URL`: Full connection string for Neon Postgres
- `OPENAI_API_KEY`: OpenAI API key for embeddings and generation

### Optional Variables

- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS
- `DEBUG`: Set to "True" for debug mode (default: False)
- `QDRANT_COLLECTION_NAME`: Name of the collection to use (default: textbook_chunks)

## Health Checks

The `/status` endpoint provides health information about all system components. Use this to verify your deployment is working correctly.

## Troubleshooting

### Common Issues

- **Connection Errors**: Verify all API keys and connection strings are correct
- **Deployment Failures**: Check the build logs in Railway dashboard
- **CORS Issues**: Ensure your frontend domain is in ALLOWED_ORIGINS

### Monitoring

- Check Railway's metrics dashboard for resource usage
- Monitor the logs for errors and performance issues
- Use the `/status` endpoint to monitor system health