from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from typing import List, Optional
from src.config import settings
from src.models.retrieved_context import RetrievedContext
import logging

logger = logging.getLogger(__name__)


class QdrantService:
    """
    Service class for interacting with Qdrant vector database
    """
    def __init__(self):
        # Initialize Qdrant client - handle both cloud and local instances
        if settings.qdrant_url.startswith("http"):
            # For Qdrant Cloud or HTTP endpoint
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )
        else:
            # For local instance (if applicable)
            self.client = QdrantClient(
                host=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )
        self.collection_name = settings.qdrant_collection_name

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: float = 0.3
    ) -> List[RetrievedContext]:
        """
        Search for similar vectors in the Qdrant collection
        """
        try:
            # Execute search - using the proper Qdrant client method
            # The search method in qdrant_client accepts the query vector directly
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True
            )

            # Convert results to RetrievedContext objects
            # Apply score threshold after search
            contexts = []
            for result in results:
                if result.score >= score_threshold:
                    payload = result.payload or {}  # Handle case where payload might be None
                    context = RetrievedContext(
                        id=str(result.id),
                        content=payload.get('content', ''),
                        url=payload.get('url', ''),
                        section=payload.get('section', ''),
                        chunk_id=payload.get('chunk_id', ''),
                        score=result.score
                    )
                    contexts.append(context)

            return contexts

        except Exception as e:
            logger.error(f"Error searching Qdrant: {str(e)}")
            raise

    def check_connection(self) -> bool:
        """
        Check if the Qdrant connection is working
        """
        try:
            # Try to get collection info to verify connection
            collection_info = self.client.get_collection(self.collection_name)
            return True
        except Exception as e:
            logger.error(f"Qdrant connection failed: {str(e)}")
            return False

    def get_all_collections(self) -> List[str]:
        """
        Get list of all collections in Qdrant
        """
        try:
            collections = self.client.get_collections()
            return [collection.name for collection in collections.collections]
        except Exception as e:
            logger.error(f"Error getting collections: {str(e)}")
            return []


# Global instance
qdrant_service = QdrantService()