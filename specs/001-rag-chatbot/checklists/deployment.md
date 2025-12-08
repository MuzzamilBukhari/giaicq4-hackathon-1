# Deployment Checklist: RAG Chatbot Integration

**Purpose**: Validate deployment and testing of the RAG system before going live
**Created**: 2025-12-08
**Feature**: [specs/001-rag-chatbot/spec.md](specs/001-rag-chatbot/spec.md)

## Pre-Deployment Setup

- [ ] Qdrant Cloud account created and cluster provisioned
- [ ] Neon Postgres account created and project set up
- [ ] OpenAI API key obtained with sufficient quota
- [ ] GitHub repository created with all code pushed
- [ ] Railway account created and linked to GitHub

## Backend Deployment

- [ ] Railway project created from GitHub repository
- [ ] Environment variables configured in Railway:
  - [ ] QDRANT_URL
  - [ ] QDRANT_API_KEY
  - [ ] NEON_DB_URL
  - [ ] OPENAI_API_KEY
  - [ ] ALLOWED_ORIGINS
- [ ] Backend successfully deployed to Railway
- [ ] Railway deployment URL obtained

## Service Validation

- [ ] Health check endpoint accessible (`/status`)
- [ ] API returns healthy status with Qdrant and Neon connections
- [ ] Metrics endpoint accessible (`/metrics`)
- [ ] Rate limiting functioning properly
- [ ] CORS configured correctly for allowed origins

## Content Indexing

- [ ] Textbook content in `/docs/` directory verified
- [ ] Indexing script tested with sample content
- [ ] Vector database populated with textbook content
- [ ] Vector count matches expected number of documents
- [ ] Metadata properly stored in Neon Postgres

## Query Functionality Testing

- [ ] Full retrieval queries return relevant answers
- [ ] Selected text queries work correctly
- [ ] Citations properly linked to source documents
- [ ] Response times under 5 seconds for most queries
- [ ] Empty query results handled gracefully

## Frontend Integration

- [ ] Docusaurus chat widget appears on all textbook pages
- [ ] Widget connects to deployed backend API
- [ ] Selected text detection works properly
- [ ] Answer display with citations renders correctly
- [ ] Loading and error states handled properly

## Performance Validation

- [ ] Average response time under 3 seconds
- [ ] 95th percentile response time under 5 seconds
- [ ] Success rate above 95%
- [ ] System handles concurrent users without degradation
- [ ] Rate limiting prevents abuse effectively

## Security Validation

- [ ] Only allowed origins can access the API
- [ ] No sensitive information exposed in frontend
- [ ] API keys properly secured in environment variables
- [ ] Proper error messages don't expose internal details

## Documentation Validation

- [ ] Deployment guide accurate and complete
- [ ] API documentation reflects actual endpoints
- [ ] Troubleshooting guide covers common issues
- [ ] Indexing instructions clear and accurate

## Production Readiness

- [ ] Monitoring and logging properly configured
- [ ] Backup procedures established for databases
- [ ] Scaling settings appropriate for expected load
- [ ] Health check endpoints for monitoring tools
- [ ] Rollback plan documented

## Final Validation

- [ ] End-to-end testing completed with full textbook content
- [ ] All integration tests passing
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] User acceptance testing completed

## Notes

- All validation steps must pass before going live
- Document any deviations from expected behavior
- Ensure rollback procedures are tested and ready