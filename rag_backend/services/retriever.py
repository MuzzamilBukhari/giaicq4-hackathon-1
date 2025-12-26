import qdrant_client
from qdrant_client.http import models
import os
from typing import List, Dict, Any

async def retrieve_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve relevant text chunks from Qdrant based on the query.
    """
    from .embeddings import generate_embedding

    try:
        # Initialize Qdrant client with environment variables
        client = qdrant_client.QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        collection_name = os.getenv("QDRANT_COLLECTION", "book_chunks")

        # Generate embedding for the query
        query_embedding = await generate_embedding(query)

        # Search in Qdrant
        search_results = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Extract relevant information from results
        chunks = []
        for result in search_results:
            chunk = {
                "text": result.payload.get("text", ""),
                "metadata": {
                    "module": result.payload.get("module", ""),
                    "section": result.payload.get("section", ""),
                    "title": result.payload.get("title", ""),
                    "url": result.payload.get("url", "")
                }
            }
            chunks.append(chunk)

        return chunks
    except Exception as e:
        print(f"Error retrieving chunks: {e}")
        raise