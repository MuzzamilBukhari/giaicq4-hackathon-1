# Research: Book Website Ingestion for RAG

## Decision: Web Scraping Approach for Docusaurus Sites
**Rationale**: Docusaurus generates static HTML sites, making them suitable for scraping with requests and BeautifulSoup. This approach allows us to extract clean text content while respecting robots.txt and handling rate limiting appropriately.
**Alternatives considered**:
- Using Docusaurus API (not available for deployed sites)
- Direct access to source markdown (not available for deployed sites)
- Third-party scraping services (unnecessary complexity)

## Decision: Text Extraction Method
**Rationale**: Using BeautifulSoup to extract text content from HTML, focusing on main content areas while filtering out navigation, headers, and footers. This provides clean text suitable for embedding generation.
**Alternatives considered**:
- Generic HTML-to-text conversion (lower quality)
- Custom CSS selectors per site (not scalable)
- Headless browser automation (unnecessary overhead)

## Decision: Content Chunking Strategy
**Rationale**: Using a sliding window approach with configurable chunk size and overlap to ensure deterministic chunking. This preserves context while maintaining consistent chunk boundaries across runs.
**Alternatives considered**:
- Sentence-based chunking (less predictable sizes)
- Paragraph-based chunking (could result in very large chunks)
- Character-based chunking with fixed windows (less context-aware)

## Decision: Cohere Embedding Model
**Rationale**: Using Cohere's embed-english-v3.0 model which is optimized for retrieval tasks and provides good performance for text similarity.
**Alternatives considered**:
- OpenAI embeddings (would violate constraint of using Cohere)
- Self-hosted models (would violate constraint of using Cohere)
- Other Cohere models (v3.0 is current best for retrieval)

## Decision: Qdrant Collection Structure
**Rationale**: Creating a dedicated collection for book content with structured metadata fields (url, section, chunk_id) to enable efficient retrieval and filtering.
**Alternatives considered**:
- Generic collection with minimal metadata (would not meet requirements)
- Multiple collections per book (unnecessary complexity)
- Different vector database (would violate constraint of using Qdrant)

## Decision: Duplicate Prevention Strategy
**Rationale**: Using the URL and chunk_id combination as a unique identifier to prevent duplicate entries. Storing a hash of the content to detect updates and only re-ingest changed content.
**Alternatives considered**:
- No duplicate prevention (would violate requirements)
- Simple URL-based deduplication (would not handle updated content)
- Timestamp-based approach (less reliable than content hashing)

## Decision: Error Handling and Resilience
**Rationale**: Implementing retry mechanisms with exponential backoff for API calls and network requests, with graceful degradation when individual pages fail.
**Alternatives considered**:
- Fail-fast approach (would be too brittle)
- No retries (would be too brittle)
- Fixed-interval retries (exponential backoff is more efficient)

## Decision: Configuration Management
**Rationale**: Using environment variables and a settings module to manage API keys, URLs, and other configuration parameters. This allows for easy deployment across different environments.
**Alternatives considered**:
- Hardcoded values (not maintainable)
- Command-line arguments only (not flexible enough)
- Configuration files (more complex than needed)