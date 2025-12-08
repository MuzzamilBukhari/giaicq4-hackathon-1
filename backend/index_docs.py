#!/usr/bin/env python3
"""
Script to index documentation files into the RAG system
"""
import asyncio
import argparse
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent))

from app.indexer import DocumentIndexer
from app.config import settings
from app.db_meta import db_manager
from app.retriever import qdrant_manager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main():
    parser = argparse.ArgumentParser(description='Index documentation files')
    parser.add_argument(
        '--docs-path',
        type=str,
        default='../docusaurus-project/docs',
        help='Path to documentation directory'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=600,
        help='Chunk size in tokens'
    )
    parser.add_argument(
        '--overlap',
        type=int,
        default=80,
        help='Overlap between chunks in tokens'
    )

    args = parser.parse_args()

    docs_path = Path(args.docs_path)
    if not docs_path.exists():
        logging.error(f"Documentation path does not exist: {docs_path}")
        sys.exit(1)

    logging.info(f"Starting indexing process...")
    logging.info(f"Docs path: {docs_path}")
    logging.info(f"Chunk size: {args.chunk_size}")
    logging.info(f"Overlap: {args.overlap}")

    # Initialize connections
    logging.info("Connecting to Qdrant...")
    await qdrant_manager.connect()
    qdrant_manager.ensure_collection_exists()

    logging.info("Connecting to Neon...")
    await db_manager.connect()
    await db_manager.create_tables()

    # Create indexer and run
    indexer = DocumentIndexer()
    
    try:
        job_id = await indexer.index_directory(
            docs_path=str(docs_path),
            chunk_size=args.chunk_size,
            overlap=args.overlap
        )
        
        logging.info(f"Indexing completed successfully! Job ID: {job_id}")
        
    except Exception as e:
        logging.error(f"Indexing failed: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        await db_manager.disconnect()

    logging.info("Done!")


if __name__ == "__main__":
    asyncio.run(main())
