# Data Model: RAG Chatbot Integration

## Entities

### 1. Textbook Content Chunk

**Description**: Represents a segment of textbook content that has been processed and stored for retrieval

**Fields**:
- `id` (UUID): Unique identifier for the database record
- `vector_id` (TEXT): Identifier that corresponds to the vector in Qdrant
- `doc_path` (TEXT): Path to the source document (e.g., `/docs/module-1/introduction.md`)
- `heading` (TEXT): The heading or section title of this content chunk
- `excerpt` (TEXT): The actual content text of the chunk
- `token_count` (INTEGER): Number of tokens in the excerpt
- `created_at` (TIMESTAMP): When this chunk was created/indexed

**Validation rules**:
- `doc_path` must be a valid path under `/docs/`
- `excerpt` must not be empty
- `token_count` must be between 500-800 tokens (per requirements)
- `vector_id` must be unique

### 2. Query Request

**Description**: Represents a user's request to the RAG system

**Fields**:
- `question` (TEXT): The user's question about the textbook content
- `selected_text` (TEXT, optional): Text that the user has highlighted (for selected-text mode)
- `mode` (ENUM): Query mode - either 'full_retrieval' or 'selected_text_only'
- `user_context` (JSON, optional): Additional context about the user's session

**Validation rules**:
- `question` must not be empty
- If `mode` is 'selected_text_only', `selected_text` must not be empty
- `mode` must be one of the allowed values

### 3. Answer Response

**Description**: The system's response to a user's query

**Fields**:
- `answer` (TEXT): The AI-generated answer to the user's question
- `sources` (ARRAY of OBJECT): List of source documents used to generate the answer
  - `doc_path` (TEXT): Path to the source document
  - `heading` (TEXT): Heading of the relevant section
  - `excerpt` (TEXT): The specific text excerpt used
  - `score` (FLOAT): Relevance score from vector search (0.0-1.0)
- `meta` (OBJECT): Metadata about the response
  - `latency_ms` (INTEGER): Time taken to generate the response
  - `model` (TEXT): The model used for generation
  - `retrieval_count` (INTEGER): Number of chunks retrieved for the answer

**Validation rules**:
- `answer` must not be empty
- Each source must have valid `doc_path`, `heading`, and `excerpt`
- Scores must be between 0.0 and 1.0

### 4. Indexing Job

**Description**: Represents an indexing operation to process textbook content

**Fields**:
- `id` (UUID): Unique identifier for the indexing job
- `status` (ENUM): Current status - 'pending', 'in_progress', 'completed', 'failed'
- `docs_path` (TEXT): Path to the documentation to be indexed
- `chunk_size` (INTEGER): Size of chunks in tokens (default 600)
- `overlap` (INTEGER): Overlap between chunks in tokens (default 80)
- `total_chunks` (INTEGER): Total number of chunks to process
- `processed_chunks` (INTEGER): Number of chunks processed so far
- `started_at` (TIMESTAMP): When the job was started
- `completed_at` (TIMESTAMP, optional): When the job was completed

**Validation rules**:
- `docs_path` must be a valid path
- `chunk_size` must be between 500-800
- `overlap` must be between 50-120
- `status` must be one of the allowed values

## Relationships

1. **Textbook Content Chunk** is created by **Indexing Job**
   - One indexing job can create many content chunks
   - Foreign key: `indexing_job_id` (optional, for tracking)

2. **Answer Response** references multiple **Textbook Content Chunk** objects through the `sources` array
   - Each source in the answer links back to a specific chunk via `vector_id` → `doc_path` + `heading`

## State Transitions

### Indexing Job States
```
pending → in_progress → completed
              ↓
            failed
```

- `pending`: Job created but not yet started
- `in_progress`: Processing chunks, `processed_chunks` increments as work progresses
- `completed`: All chunks processed successfully
- `failed`: Error occurred during processing

## Constraints

1. **Referential Integrity**: Each source in an answer must correspond to an existing Textbook Content Chunk
2. **Content Integrity**: Content chunks must preserve the original meaning of the textbook content
3. **Token Count Validation**: All chunks must adhere to the 500-800 token range with appropriate overlap
4. **Path Validation**: All document paths must be under the `/docs/` directory
5. **Citation Accuracy**: Sources in answers must accurately reference the original content chunks