# Update Index

This guide explains how to update the document index when textbook content changes.

## Overview

The indexing system processes markdown files from the `/docs/` directory and stores them as vector embeddings in Qdrant with metadata in Neon Postgres. When content changes, you need to update the index to reflect the changes.

## Running the Indexer

### Prerequisites

Make sure you have the required environment variables set:
- `QDRANT_URL` and `QDRANT_API_KEY`
- `NEON_DB_URL`
- `OPENAI_API_KEY`

### Basic Indexing

To index all documents in the default location (`../docs`):

```bash
cd backend
python scripts/index_docs.py
```

### Custom Parameters

You can customize the indexing process with various parameters:

```bash
python scripts/index_docs.py \
  --docs-path /path/to/docs \
  --chunk-size 600 \
  --overlap 80 \
  --replace
```

### Parameters

- `--docs-path`: Path to the documentation directory (default: `../docs`)
- `--chunk-size`: Size of text chunks in tokens (default: 600, range: 500-800)
- `--overlap`: Overlap between chunks in tokens (default: 80, range: 50-120)
- `--replace`: Replace existing index (default: upserts only)
- `--sample`: Run on a sample of files for testing (default: False)

## Indexing Process

### 1. Document Parsing

The system parses all markdown files in the specified directory, extracting headings and content.

### 2. Text Processing

- Documents are cleaned of markdown formatting that might interfere with embeddings
- Content is split into chunks of specified size with overlap
- Token counts are validated to ensure they're within the required range

### 3. Embedding Generation

Each text chunk is converted to a vector embedding using OpenAI's text-embedding-3-small model.

### 4. Storage

- Vector embeddings are stored in Qdrant with document metadata in the payload
- Document metadata (path, heading, excerpt, token count) is stored in Neon Postgres
- An indexing job record is created to track progress

## Incremental Updates

The system supports incremental updates, meaning you can add new documents or update existing ones without reindexing everything. By default, the indexer upserts documents, which means it adds new ones and updates existing ones.

To completely replace the index, use the `--replace` flag.

## Sample Mode

For testing purposes, you can run the indexer in sample mode:

```bash
python scripts/index_docs.py --sample
```

This processes only a few files to verify the indexing process works correctly.

## Monitoring Indexing Jobs

The system creates indexing job records that you can monitor:

- Each job has a unique ID and tracks progress
- Status is updated as chunks are processed
- You can query job status to see completion percentage

## Troubleshooting

### Common Issues

- **Token Count Validation**: Chunks outside the 500-800 token range will generate warnings
- **API Limits**: Large document sets may hit OpenAI rate limits
- **Connection Issues**: Verify Qdrant and Neon connections are working

### Verification

After indexing, verify the process completed successfully:

1. Check the indexing job status
2. Verify vector count increased in Qdrant
3. Confirm metadata exists in Neon Postgres
4. Test queries to ensure new content is searchable