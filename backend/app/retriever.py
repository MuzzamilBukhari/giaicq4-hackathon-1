from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from .config import settings
import logging
from uuid import uuid4


class QdrantManager:
    def __init__(self):
        self.client = None
        self.collection_name = settings.qdrant_collection_name

    async def connect(self):
        """Initialize Qdrant client connection"""
        try:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                prefer_grpc=False  # Using HTTP for simplicity
            )
            logging.info(f"Connected to Qdrant at {settings.qdrant_url}")
        except Exception as e:
            logging.error(f"Failed to connect to Qdrant: {e}")
            raise

    def ensure_collection_exists(self):
        """Ensure the collection exists with proper configuration"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with 1536-dimensional vectors for OpenAI embeddings
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # OpenAI embedding dimension
                        distance=models.Distance.COSINE
                    ),
                    # Store metadata for provenance
                    on_disk_payload=True
                )
                logging.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logging.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logging.error(f"Failed to ensure collection exists: {e}")
            raise

    def upsert_vectors(self, vectors: List[Dict[str, Any]]):
        """
        Upsert vectors to Qdrant with metadata
        Each vector dict should contain:
        - id: unique identifier
        - vector: the embedding vector
        - payload: metadata dict with doc_path, heading, excerpt, token_count, created_at
        """
        points = []
        for item in vectors:
            point = models.PointStruct(
                id=item["id"],
                vector=item["vector"],
                payload=item["payload"]
            )
            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        logging.info(f"Upserted {len(points)} vectors to Qdrant")

    def search_vectors(self, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant
        Returns list of points with payload and score
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )

        # Format results to include required fields
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            })

        return formatted_results

    async def delete_collection(self):
        """Delete the collection (for testing/development)"""
    def delete_collection(self):
        """Delete the collection (for testing/development)"""
        try:
            self.client.delete_collection(self.collection_name)
            logging.info(f"Deleted Qdrant collection: {self.collection_name}")
        except Exception as e:
            logging.error(f"Failed to delete collection: {e}")

    def get_vector_count(self) -> int:
        """Get the total number of vectors in the collection"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            logging.error(f"Failed to get vector count: {e}")
            return 0


# Global Qdrant manager instance
qdrant_manager = QdrantManager()