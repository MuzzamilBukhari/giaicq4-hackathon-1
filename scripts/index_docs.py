#!/usr/bin/env python3
"""
CLI script for indexing textbook content into the RAG system
"""
import argparse
import asyncio
import os
from pathlib import Path
from typing import List
import logging

# Add the backend directory to the path so we can import our modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.indexer import embedder_adapter
from app.db_meta import db_manager
from app.retriever import qdrant_manager


async def index_docs(
    docs_path: str,
    chunk_size: int = 600,
    overlap: int = 80,
    replace: bool = False,
    sample: bool = False
) -> dict:
    """
    Index documents from the specified path
    """
    print(f"Starting indexing process for: {docs_path}")
    print(f"Chunk size: {chunk_size}, Overlap: {overlap}, Replace: {replace}, Sample: {sample}")

    # Connect to services
    await qdrant_manager.connect()
    await qdrant_manager.ensure_collection_exists()
    await db_manager.connect()
    await db_manager.create_tables()

    # Get all markdown files
    docs_dir = Path(docs_path)
    if not docs_dir.exists():
        raise FileNotFoundError(f"Documents directory does not exist: {docs_path}")

    # Find all markdown files
    if sample:
        # For sample mode, just process a few files
        md_files = list(docs_dir.rglob("*.md"))[:3]  # Only first 3 files for sample
        print(f"Sample mode: processing {len(md_files)} files")
    else:
        md_files = list(docs_dir.rglob("*.md"))
        print(f"Found {len(md_files)} markdown files to process")

    if not md_files:
        print("No markdown files found to process")
        return {"status": "completed", "processed_files": 0, "total_chunks": 0}

    # Create indexing job record
    total_files = len(md_files) if not sample else min(len(md_files), 1)
    estimated_total_chunks = total_files * 10  # Rough estimate - will be updated as we process
    job_id = await db_manager.create_indexing_job(docs_path, chunk_size, overlap, estimated_total_chunks)
    print(f"Created indexing job: {job_id}")

    total_chunks = 0
    processed_files = 0
    errors = []

    for md_file in md_files:
        try:
            print(f"Processing: {md_file}")

            # Process the document
            chunks = await embedder_adapter.process_document(
                str(md_file),
                chunk_size=chunk_size,
                overlap=overlap
            )

            print(f"  Generated {len(chunks)} chunks")

            # Upsert to Qdrant and DB with job tracking
            await embedder_adapter.upsert_chunks_to_qdrant_and_db(chunks, job_id)

            total_chunks += len(chunks)
            processed_files += 1

            # For sample mode, break after first file
            if sample:
                break

        except Exception as e:
            error_msg = f"Error processing {md_file}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
            continue

    # Update job status to completed
    await db_manager.update_indexing_job_status(job_id, "completed", total_chunks)

    print(f"Indexing completed. Processed {processed_files} files, created {total_chunks} chunks.")

    if errors:
        print(f"Encountered {len(errors)} errors during indexing.")
        for error in errors:
            print(f"  - {error}")

    return {
        "status": "completed" if not errors else "completed_with_errors",
        "processed_files": processed_files,
        "total_chunks": total_chunks,
        "errors": errors
    }


def main():
    parser = argparse.ArgumentParser(description="Index textbook content for RAG system")
    parser.add_argument(
        "--docs-path",
        type=str,
        default="../docs",
        help="Path to the documentation to be indexed (default: ../docs)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=600,
        help="Size of chunks in tokens (default: 600, range: 500-800)"
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=80,
        help="Overlap between chunks in tokens (default: 80, range: 50-120)"
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing index (default: False, upserts only)"
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Run in sample mode with just a few files (default: False)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not (500 <= args.chunk_size <= 800):
        print(f"Error: chunk-size must be between 500 and 800, got {args.chunk_size}")
        return 1

    if not (50 <= args.overlap <= 120):
        print(f"Error: overlap must be between 50 and 120, got {args.overlap}")
        return 1

    # Run the indexing process
    try:
        result = asyncio.run(
            index_docs(
                docs_path=args.docs_path,
                chunk_size=args.chunk_size,
                overlap=args.overlap,
                replace=args.replace,
                sample=args.sample
            )
        )

        print(f"\nIndexing result: {result}")
        return 0
    except Exception as e:
        print(f"Fatal error during indexing: {e}")
        return 1


if __name__ == "__main__":
    exit(main())