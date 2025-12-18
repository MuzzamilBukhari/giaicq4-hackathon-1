# Data Model: Book Website Ingestion for RAG

## Content Chunk Entity
**Description**: Represents a segment of text extracted from the book website
- **Fields**:
  - `chunk_id` (string): Unique identifier for this chunk (URL-based + sequential number)
  - `content` (string): The actual text content of the chunk
  - `url` (string): Source URL where this content originated
  - `section` (string): Section or page title where this content appears
  - `content_hash` (string): SHA256 hash of the content for duplicate detection
  - `embedding` (list[float]): Vector embedding of the content
  - `created_at` (datetime): Timestamp when this chunk was created
  - `updated_at` (datetime): Timestamp when this chunk was last updated

## Source URL Entity
**Description**: Represents a specific page or section of the Docusaurus book website
- **Fields**:
  - `url` (string): The full URL of the page
  - `title` (string): Page title extracted from HTML
  - `section_path` (string): Hierarchical path of the section (e.g., "module-1/chapter-2")
  - `last_crawled` (datetime): Timestamp of last successful crawl
  - `status_code` (int): HTTP status code from last fetch
  - `content_length` (int): Length of content in characters

## Vector Database Record Entity
**Description**: Represents a stored record in Qdrant containing the embedding vector and metadata
- **Fields**:
  - `id` (string): Unique identifier matching the chunk_id
  - `vector` (list[float]): The embedding vector from Cohere
  - `payload` (object): Metadata object containing:
    - `url` (string): Source URL
    - `section` (string): Section name
    - `chunk_id` (string): Chunk identifier
    - `content_hash` (string): Content hash for duplicate detection
  - `created_at` (datetime): Timestamp when record was stored

## Ingestion Process Entity
**Description**: Tracks the state and progress of an ingestion run
- **Fields**:
  - `run_id` (string): Unique identifier for this ingestion run
  - `start_time` (datetime): When the ingestion started
  - `end_time` (datetime): When the ingestion completed
  - `status` (string): Current status (running, completed, failed, paused)
  - `processed_urls` (int): Count of URLs successfully processed
  - `failed_urls` (int): Count of URLs that failed to process
  - `created_chunks` (int): Count of new chunks created
  - `skipped_chunks` (int): Count of chunks skipped due to duplication
  - `error_log` (list): List of errors encountered during the run

## Validation Rules
- Content chunks must have non-empty content (min 10 characters)
- URLs must be valid and accessible
- Embeddings must be generated successfully before storage
- Chunk_id must be unique within the system
- Content hash must be calculated using SHA256 algorithm
- Metadata fields (url, section, chunk_id) must not be empty

## Relationships
- One Source URL can generate multiple Content Chunks
- One Content Chunk maps to one Vector Database Record
- One Ingestion Process manages multiple Content Chunks