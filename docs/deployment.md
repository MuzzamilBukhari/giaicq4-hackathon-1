# Deployment Guide

This guide provides instructions for deploying the RAG Backend Service in various environments.

## Prerequisites

Before deploying the RAG Backend Service, ensure you have:

- **Qdrant Cloud Account**: Access to a Qdrant Cloud instance with pre-populated book embeddings
- **Google Gemini API Key**: Valid API key for Google's Gemini service
- **Server Resources**: Minimum 2GB RAM and 2 CPU cores (recommended 4GB RAM and 4 CPU cores)
- **Docker & Docker Compose**: For containerized deployment
- **SSL Certificate**: For production HTTPS deployment (optional but recommended)

## Environment Variables

Create a `.env` file with the following required variables:

```env
# Qdrant Configuration
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=book_content

# Google Gemini Configuration
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-1.5-pro
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# Application Configuration
CORS_ORIGINS=["https://your-docusaurus-site.com"]
LOG_LEVEL=info

# Production Configuration
ENVIRONMENT=production
DEBUG=False
```

## Deployment Options

### 1. Docker Compose (Recommended for Production)

#### Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-backend-service
   ```

2. Create your `.env` file with the environment variables above

3. Deploy using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Verify the deployment:
   ```bash
   docker-compose logs rag-backend
   ```

#### Production Considerations

- **SSL/HTTPS**: Update the `docker-compose.yml` to include SSL configuration
- **Volume Mounts**: Ensure logs and configuration are properly mounted
- **Health Checks**: Monitor the service using the health endpoint
- **Resource Limits**: Set appropriate memory and CPU limits

### 2. Direct Python Deployment

#### Prerequisites

- Python 3.9 or higher
- Virtual environment tool (venv or conda)

#### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-backend-service
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

### 3. Kubernetes Deployment

For Kubernetes deployments, use the provided Docker image and create appropriate Kubernetes manifests. The service should be deployed with:

- Resource requests and limits
- Liveness and readiness probes
- Horizontal Pod Autoscaler
- ConfigMap for environment variables
- Secret for API keys

## Configuration Options

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_URL` | - | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | - | Qdrant API key |
| `QDRANT_COLLECTION_NAME` | `book_content` | Name of the Qdrant collection |
| `GOOGLE_API_KEY` | - | Google API key for Gemini |
| `GEMINI_MODEL` | `gemini-1.5-pro` | Gemini model to use |
| `GEMINI_BASE_URL` | - | OpenAI-compatible endpoint for Gemini |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed origins for CORS |
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) |
| `ENVIRONMENT` | `development` | Environment (development, staging, production) |
| `DEBUG` | `False` | Enable debug mode |
| `MAX_REQUEST_SIZE` | 10485760 (10MB) | Maximum request size in bytes |
| `REQUEST_TIMEOUT` | 30 | Request timeout in seconds |
| `MAX_CONTEXT_CHUNKS` | 10 | Maximum number of context chunks to retrieve |
| `RATE_LIMIT_REQUESTS` | 100 | Rate limit requests per minute per IP |

## Scaling

### Horizontal Scaling

The service is stateless and can be scaled horizontally. Consider the following when scaling:

- Qdrant connection pooling
- Rate limiting per IP across instances
- Load balancer configuration

### Vertical Scaling

For increased performance, consider:

- Increasing memory allocation
- Increasing CPU allocation
- Optimizing Qdrant query parameters

## Monitoring

Monitor the following endpoints:

- Health: `GET /api/v1/health`
- Ready: `GET /api/v1/ready`

Key metrics to monitor:

- Response time
- Error rates
- Qdrant connection status
- Gemini API connection status
- Rate limit hits

## Security

### API Keys

- Store API keys as environment variables or secrets
- Never commit API keys to version control
- Rotate API keys regularly

### Network Security

- Use HTTPS in production
- Restrict access to the API as needed
- Implement proper CORS configuration

### Rate Limiting

The service includes built-in rate limiting (100 requests per minute per IP by default). Adjust as needed for your use case.

## Troubleshooting

### Common Issues

#### Service Won't Start
- Check that all required environment variables are set
- Verify Qdrant connection details
- Verify Gemini API key and endpoint

#### No Results from Queries
- Verify Qdrant collection name is correct
- Check that embeddings exist in the Qdrant collection
- Verify the query is properly formatted

#### Slow Response Times
- Check Qdrant performance
- Verify sufficient server resources
- Consider optimizing the number of retrieved chunks

#### CORS Errors
- Verify `CORS_ORIGINS` is properly configured
- Check that frontend domain matches allowed origins

### Logs

Check application logs for detailed error information. When using Docker Compose:

```bash
docker-compose logs rag-backend
```

### Health Checks

Use the health endpoint to verify service status:

```bash
curl http://your-server:8000/api/v1/health
```

## Updates

To update the service:

1. Pull the latest code
2. If using Docker Compose, run:
   ```bash
   docker-compose pull
   docker-compose up -d
   ```
3. Verify the updated service is working

## Rollback

To rollback to a previous version:

1. If using Git, checkout the previous commit
2. If using Docker, use a previous image tag
3. Redeploy the service