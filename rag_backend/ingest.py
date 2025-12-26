#!/usr/bin/env python3
"""
Ingestion script for the RAG Chatbot system.
Reads markdown docs, chunks them, generates embeddings, and uploads to Qdrant.
"""

import os
import asyncio
import glob
from pathlib import Path
from dotenv import load_dotenv
import qdrant_client
from qdrant_client.http import models
from services.embeddings import generate_embeddings
from utils.chunking import chunk_text, extract_metadata_from_path
from utils.markdown_cleaning import clean_markdown_content
import uuid

# Load environment variables
load_dotenv()

# Initialize Qdrant client
client = qdrant_client.QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)
collection_name = os.getenv("QDRANT_COLLECTION", "book_chunks")

async def create_qdrant_collection():
    """Create Qdrant collection with proper configuration."""
    try:
        # Check if collection already exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if collection_name in collection_names:
            print(f"Collection '{collection_name}' already exists. Skipping creation.")
            return

        # Create collection
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),  # Gemini embedding size is 768
        )
        print(f"Created Qdrant collection: {collection_name}")
    except Exception as e:
        print(f"Error creating Qdrant collection: {e}")
        raise

async def process_markdown_file(file_path: str):
    """Process a single markdown file: clean, chunk, embed, and upload."""
    print(f"Processing file: {file_path}")

    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Clean the content
        cleaned_content = clean_markdown_content(content)

        # Extract metadata from path
        path_metadata = extract_metadata_from_path(file_path)

        # Extract title from content
        from utils.markdown_cleaning import extract_title_from_markdown
        title = extract_title_from_markdown(content)
        if not path_metadata["section"]:
            path_metadata["section"] = title or Path(file_path).stem

        # Chunk the content
        chunks = chunk_text(cleaned_content)

        # Prepare for embedding and upload
        texts_to_embed = []
        payloads = []

        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) == 0:
                continue

            # Create payload with metadata
            payload = {
                "text": chunk,
                "module": path_metadata["module"],
                "chapter": path_metadata["chapter"],
                "section": path_metadata["section"],
                "title": title,
                "url": path_metadata["url"],
                "source_file": file_path,
                "chunk_index": i
            }

            texts_to_embed.append(chunk)
            payloads.append(payload)

        if not texts_to_embed:
            print(f"No content to process for {file_path}")
            return

        # Generate embeddings
        print(f"Generating embeddings for {len(texts_to_embed)} chunks...")
        embeddings = await generate_embeddings(texts_to_embed)

        # Prepare points for Qdrant
        points = []
        for i, (embedding, payload) in enumerate(zip(embeddings, payloads)):
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload
            )
            points.append(point)

        # Upload to Qdrant
        print(f"Uploading {len(points)} points to Qdrant...")
        client.upsert(
            collection_name=collection_name,
            points=points
        )

        print(f"Successfully processed {file_path}: {len(points)} chunks uploaded")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        raise

async def main():
    """Main ingestion function."""
    print("Starting ingestion process...")

    # Create Qdrant collection if it doesn't exist
    await create_qdrant_collection()

    # Find all markdown files in docs directory
    docs_path = "docs/**/*.md"
    if not os.path.exists("docs"):
        print("Docs directory not found. Looking for markdown files in current directory...")
        docs_path = "**/*.md"

    markdown_files = glob.glob(docs_path, recursive=True)

    if not markdown_files:
        print("No markdown files found. Looking in common documentation directories...")
        possible_paths = [
            "documentation/**/*.md",
            "content/**/*.md",
            "textbook/**/*.md",
            "source/**/*.md"
        ]
        for path in possible_paths:
            markdown_files = glob.glob(path, recursive=True)
            if markdown_files:
                break

    if not markdown_files:
        print("No markdown files found to process.")
        return

    print(f"Found {len(markdown_files)} markdown files to process")

    # Process files one by one
    for file_path in markdown_files:
        try:
            await process_markdown_file(file_path)
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
            continue  # Continue with other files even if one fails

    print("Ingestion process completed!")

if __name__ == "__main__":
    asyncio.run(main())