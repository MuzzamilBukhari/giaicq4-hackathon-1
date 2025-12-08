# Research Summary: RAG Chatbot Integration

## Decisions Documented

### 1. Embedding Model & Vector Size Selection

**Decision**: Use OpenAI text-embedding-3-small model with 1536-dimensional vectors

**Rationale**: The OpenAI text-embedding-3-small model offers a good balance of performance and cost. It provides high-quality embeddings suitable for semantic search while being more cost-effective than larger models. The 1536-dimensional vector size is well-supported by Qdrant and provides good retrieval accuracy.

**Alternatives considered**:
- text-embedding-ada-002 (1536-dim): Still good but older model
- text-embedding-3-large (3072-dim): Higher quality but more expensive and slower
- Cohere embeddings: Alternative but ChatKit SDK integration is optimized for OpenAI

### 2. Chunking Policy

**Decision**: Fixed chunk size of 600 tokens with 80 token overlap

**Rationale**: 600 tokens provides a good balance between context richness and retrieval precision. The 80-token overlap ensures that semantic boundaries aren't broken while avoiding excessive duplication. This is within the specified range of 500-800 tokens with 50-120 overlap.

**Alternatives considered**:
- Adaptive chunking: More complex to implement, potential for inconsistent retrieval
- Smaller chunks (400 tokens): Might lose context
- Larger chunks (900+ tokens): Might dilute semantic meaning

### 3. Qdrant Collection Parameters

**Decision**:
- Distance metric: Cosine similarity
- Replicas: 1 (for initial deployment, can scale)
- Payload fields: {doc_path, heading, excerpt, token_count, created_at}

**Rationale**: Cosine similarity is standard for semantic search and works well with OpenAI embeddings. 1 replica is sufficient for initial deployment with Railway's scaling. The payload fields match the requirements for provenance tracking.

**Alternatives considered**:
- Euclidean distance: Less suitable for high-dimensional embeddings
- Dot product: Could work but cosine is more standard for text embeddings

### 4. Neon Schema Details

**Decision**:
- Table: `chunks` with fields:
  - id (UUID, primary key)
  - vector_id (TEXT, references Qdrant point ID)
  - doc_path (TEXT, path to source document)
  - heading (TEXT, heading of the section)
  - excerpt (TEXT, the actual content chunk)
  - token_count (INTEGER, number of tokens in chunk)
  - created_at (TIMESTAMP, when record was created)
- Retention: Keep all metadata indefinitely (no automatic cleanup)

**Rationale**: This schema captures all required metadata for provenance and allows efficient lookups by vector_id or doc_path. The UUID primary key provides uniqueness, and the vector_id allows linking to Qdrant vectors.

**Alternatives considered**:
- Different field types: TEXT is appropriate for content and paths
- Automatic cleanup: Could be added later if needed, but initial approach keeps all metadata

### 5. ChatKit Agent Design

**Decision**: Single retrieval-augmented agent approach

**Rationale**: A single agent that performs both retrieval and synthesis is simpler to implement and maintain. The ChatKit Agents SDK allows us to create a structured agent that can call our retriever service and then synthesize the response with proper citations.

**Agent flow**:
1. Receive user query
2. Call retriever service to get top-k relevant chunks
3. Format retrieved context with query into a structured prompt
4. Generate response with citations using ChatKit
5. Return structured JSON with answer and sources

**Prompt template elements**:
- System message with citation requirements
- Retrieved context from vector search
- User query
- Request for structured output with sources

**Alternatives considered**:
- Multi-agent pipeline: More complex but potentially more modular
- Separate retriever + synthesizer: Could provide more control but adds complexity

### 6. Failure Mode Behavior

**Decision**:
- When retrieval returns empty results: Return a response indicating no relevant content was found in the textbook
- When confidence is low: Still provide answer but with appropriate caveats
- When system is unavailable: Return appropriate error message to user

**Rationale**: This approach is transparent with users about system capabilities and limitations, preventing hallucinations while maintaining trust.

**Alternatives considered**:
- Generic responses: Less helpful for users
- Partial answers without caveats: Could mislead users

### 7. Deployment Choices on Railway

**Decision**:
- Docker-based deployment for consistency
- Environment variables for secrets management
- Standard health checks on /status endpoint
- Auto-scaling based on Railway defaults

**Rationale**: Docker provides consistent deployments across environments. Railway's environment variable system securely manages secrets. The /status endpoint provides basic health monitoring.

**Alternatives considered**:
- Railway's native build: Less control over dependencies
- Alternative hosting: Railway was specified in requirements

### 8. CI Behavior

**Decision**:
- Run unit tests on all PRs
- Run small sample index integration test on PRs (using mocked embeddings)
- Full indexing only in staging/prod on-demand
- Validate API contract compliance

**Rationale**: This provides fast feedback on PRs while avoiding expensive full indexing operations during development. The sample test validates core functionality without requiring full content.

**Alternatives considered**:
- Full indexing on PRs: Too expensive and time-consuming
- No integration tests: Would miss integration issues