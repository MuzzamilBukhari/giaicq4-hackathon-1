# Troubleshooting

This guide provides solutions to common issues with the RAG Chatbot system.

## Common Issues

### API Connection Errors

**Symptoms**:
- 500 errors when querying
- "Failed to connect to Qdrant/Neon" messages in logs

**Solutions**:
1. Verify environment variables are set correctly:
   - `QDRANT_URL`, `QDRANT_API_KEY`
   - `NEON_DB_URL`
   - `OPENAI_API_KEY`
2. Test connections independently
3. Check network/firewall settings if self-hosting

### Empty Results

**Symptoms**:
- Queries return "no relevant content found" messages
- Vector search returns no results

**Solutions**:
1. Verify documents have been indexed:
   - Check vector count with `python scripts/qdrant_manage.py --count`
   - Verify metadata exists in Neon
2. Test with simple, known content
3. Check chunking parameters (500-800 token range)

### Slow Queries

**Symptoms**:
- Query responses taking more than 5 seconds
- High latency in `/query` endpoint

**Solutions**:
1. Check system resources in Railway dashboard
2. Verify Qdrant Cloud performance tier
3. Optimize the number of retrieved chunks (currently set to 5)
4. Consider caching frequent queries

### Indexing Failures

**Symptoms**:
- Indexing process stops unexpectedly
- Error messages during indexing

**Solutions**:
1. Check logs for specific error messages
2. Verify file permissions for docs directory
3. Ensure sufficient API quota for embedding service
4. Validate markdown syntax in documents

## Health Checks

### Checking System Status

Use the `/status` endpoint to verify all components:

```bash
curl https://your-app.railway.app/status
```

Expected response includes:
- `status`: healthy/degraded
- `qdrant_ok`: boolean
- `neon_ok`: boolean
- `vector_count`: number of indexed vectors

### Database Connection

Test Neon Postgres connection:

```bash
# Check if tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';
```

### Vector Database

Test Qdrant connection and collection:

```bash
python scripts/qdrant_manage.py --list
python scripts/qdrant_manage.py --count
```

## Debugging Queries

### Verifying Index Quality

1. Check if documents are properly indexed:
   ```bash
   # Count total vectors
   python scripts/qdrant_manage.py --count
   ```

2. Test vector search manually:
   - Use Qdrant dashboard to test similarity search
   - Verify payload data is correct

### Query Testing

1. Test with simple, known questions
2. Use the sample indexing mode to test end-to-end flow
3. Check query logs for patterns

## Performance Optimization

### Caching

Consider implementing caching for frequent queries:
- Cache results for common questions
- Implement time-based cache invalidation

### Resource Monitoring

Monitor these metrics:
- API response times
- Database connection pool usage
- Vector database query performance
- Memory and CPU usage

## Environment-Specific Issues

### Railway Deployment

- Check Railway logs for deployment errors
- Verify environment variables are set at the service level
- Monitor resource usage and scale if needed

### Local Development

- Ensure Docker containers are running:
  ```bash
  docker-compose up -d
  ```
- Check that local services are accessible
- Verify `.env` file contains correct values

## Support Information

When requesting support, provide:

1. Full error messages and stack traces
2. Environment details (local/Railway, Python version)
3. Steps to reproduce the issue
4. System status from `/status` endpoint
5. Relevant logs from Railway or local environment