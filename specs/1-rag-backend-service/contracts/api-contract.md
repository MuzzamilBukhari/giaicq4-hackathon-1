# API Contracts: RAG Backend Service

**Feature**: 1-rag-backend-service
**Created**: 2025-12-17

## OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: RAG Backend Service API
  description: API for RAG chatbot functionality with Docusaurus book content
  version: 1.0.0
servers:
  - url: http://localhost:8000
    description: Development server
  - url: https://api.example.com
    description: Production server

paths:
  /chat:
    post:
      summary: Process a user query and return a RAG-generated response
      description: Accepts a user query, retrieves relevant context from Qdrant, and generates a response using Gemini
      operationId: chat
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/QueryRequest'
      responses:
        '200':
          description: Successful response with streaming content
          content:
            text/event-stream:
              schema:
                $ref: '#/components/schemas/ChatResponse'
        '400':
          description: Invalid query format or content
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '500':
          description: Internal server error during processing
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
      x-code-samples:
        - lang: curl
          source: |
            curl -X POST http://localhost:8000/chat \
              -H "Content-Type: application/json" \
              -d '{"query": "What is ROS 2?","session_id": "abc123"}'

  /health:
    get:
      summary: Health check endpoint
      description: Returns the health status of the service
      operationId: health
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "healthy"
                  timestamp:
                    type: string
                    format: date-time
                    example: "2025-12-17T10:00:00Z"

components:
  schemas:
    QueryRequest:
      type: object
      required:
        - query
      properties:
        query:
          type: string
          description: The user's question or prompt
          example: "How do I create a ROS 2 publisher?"
          minLength: 1
          maxLength: 2000
        session_id:
          type: string
          description: Optional session identifier for conversation context
          example: "sess_abc123"
          pattern: "^[a-zA-Z0-9_-]+$"
        metadata:
          type: object
          description: Additional request metadata
          additionalProperties: true

    ChatResponse:
      type: object
      required:
        - id
        - answer
        - sources
        - created_at
      properties:
        id:
          type: string
          description: Unique response identifier
          example: "resp_def456"
        answer:
          type: string
          description: The generated answer to the user's query
          example: "To create a ROS 2 publisher, you need to..."
        sources:
          type: array
          description: List of source documents used in generating the response
          items:
            type: object
            required:
              - url
              - section
              - relevance_score
            properties:
              url:
                type: string
                description: Source URL of the documentation
                example: "https://example.com/docs/ros2/publishers"
              section:
                type: string
                description: Section title from the source
                example: "Creating Publishers in ROS 2"
              relevance_score:
                type: number
                description: How relevant this source was (0.0-1.0)
                minimum: 0.0
                maximum: 1.0
                example: 0.85
        created_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp of response creation
          example: "2025-12-17T10:00:00Z"
        model:
          type: string
          description: Name of the model used
          example: "gemini-1.5-pro"
        usage:
          type: object
          description: Token usage information
          properties:
            prompt_tokens:
              type: integer
              description: Number of tokens in the prompt
              example: 150
            completion_tokens:
              type: integer
              description: Number of tokens in the completion
              example: 200
            total_tokens:
              type: integer
              description: Total number of tokens used
              example: 350

    ErrorResponse:
      type: object
      required:
        - error
        - message
      properties:
        error:
          type: string
          description: Error type identifier
          example: "invalid_query"
        message:
          type: string
          description: Human-readable error message
          example: "Query must be between 1 and 2000 characters"
        details:
          type: object
          description: Additional error details (optional)
          additionalProperties: true

  parameters:
    SessionId:
      name: session_id
      in: query
      required: false
      description: Session identifier for conversation context
      schema:
        type: string
        pattern: "^[a-zA-Z0-9_-]+$"
```

## Endpoint Specifications

### POST /chat
- **Purpose**: Process user queries with RAG capabilities
- **Authentication**: None required (public API)
- **Rate Limiting**: 100 requests per minute per IP
- **Response Type**: Server-Sent Events (SSE) for streaming
- **Timeout**: 30 seconds

### GET /health
- **Purpose**: Service health check for monitoring
- **Authentication**: None required
- **Response Type**: JSON
- **Cache**: No caching recommended

## Request/Response Patterns

### Query Processing
1. Client sends QueryRequest to `/chat`
2. Server retrieves context from Qdrant
3. Server processes with Gemini agent
4. Server streams response via SSE
5. Client receives response tokens in real-time

### Error Handling
- Invalid queries return 400 with ErrorResponse
- Processing errors return 500 with ErrorResponse
- Rate limit exceeded returns 429