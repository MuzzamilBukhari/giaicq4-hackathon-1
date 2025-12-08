#!/usr/bin/env python3
"""
Helper script to manage Qdrant collections for the RAG system
"""
import argparse
import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.retriever import qdrant_manager
from app.config import settings


async def list_collections():
    """List all Qdrant collections"""
    await qdrant_manager.connect()
    collections = await qdrant_manager.client.get_collections()

    print("Qdrant Collections:")
    for collection in collections.collections:
        info = await qdrant_manager.client.get_collection(collection.name)
        print(f"  - {collection.name} (points: {info.points_count}, vectors: {info.config.params.vectors.size})")


async def count_vectors(collection_name: str = None):
    """Count vectors in the textbook collection"""
    await qdrant_manager.connect()
    collection_name = collection_name or settings.qdrant_collection_name

    try:
        count = await qdrant_manager.get_vector_count()
        print(f"Vector count in '{collection_name}': {count}")
        return count
    except Exception as e:
        print(f"Error getting vector count: {e}")
        return None


async def create_collection(collection_name: str = None):
    """Create the textbook collection"""
    await qdrant_manager.connect()
    collection_name = collection_name or settings.qdrant_collection_name

    try:
        await qdrant_manager.ensure_collection_exists()
        print(f"Collection '{collection_name}' created or already exists")
    except Exception as e:
        print(f"Error creating collection: {e}")


async def delete_collection(collection_name: str = None):
    """Delete the textbook collection"""
    await qdrant_manager.connect()
    collection_name = collection_name or settings.qdrant_collection_name

    try:
        await qdrant_manager.client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' deleted")
    except Exception as e:
        print(f"Error deleting collection: {e}")


def main():
    parser = argparse.ArgumentParser(description="Manage Qdrant collections for RAG system")
    parser.add_argument(
        "action",
        choices=["list", "count", "create", "delete"],
        help="Action to perform on Qdrant collections"
    )
    parser.add_argument(
        "--collection",
        type=str,
        help="Collection name (defaults to configured collection name)"
    )

    args = parser.parse_args()

    try:
        if args.action == "list":
            asyncio.run(list_collections())
        elif args.action == "count":
            asyncio.run(count_vectors(args.collection))
        elif args.action == "create":
            asyncio.run(create_collection(args.collection))
        elif args.action == "delete":
            asyncio.run(delete_collection(args.collection))
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())