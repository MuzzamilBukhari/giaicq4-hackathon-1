# Quickstart: Book Website Ingestion for RAG

## Prerequisites
- Python 3.9+
- Pip package manager
- Cohere API key
- Qdrant Cloud cluster URL and API key

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   BOOK_BASE_URL=https://your-book-site.github.io
   ```

## Basic Usage

1. **Run the ingestion pipeline**
   ```bash
   python -m src.scripts.run_ingestion --base-url https://your-book-site.github.io
   ```

2. **With custom parameters**
   ```bash
   python -m src.scripts.run_ingestion \
     --base-url https://your-book-site.github.io \
     --chunk-size 512 \
     --overlap-size 64 \
     --qdrant-collection book-content
   ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `COHERE_API_KEY` | API key for Cohere embeddings service | Yes |
| `QDRANT_URL` | URL of your Qdrant cluster | Yes |
| `QDRANT_API_KEY` | API key for Qdrant cluster | Yes |
| `BOOK_BASE_URL` | Base URL of the Docusaurus book site | Yes |
| `CHUNK_SIZE` | Size of text chunks in tokens (default: 512) | No |
| `OVERLAP_SIZE` | Overlap between chunks in tokens (default: 64) | No |
| `QDRANT_COLLECTION` | Name of Qdrant collection (default: book-content) | No |

## Verification

After running the ingestion, verify the results:

1. Check the Qdrant dashboard to confirm vectors were stored
2. Verify the count of stored vectors matches expected number of chunks
3. Validate that metadata (url, section, chunk_id) is correctly associated with each vector

## Troubleshooting

- **API rate limits**: The system implements exponential backoff for API calls
- **Network errors**: Individual URL failures won't stop the entire process
- **Duplicate detection**: The system prevents re-storing identical content
- **Large sites**: For very large sites, consider running in batches