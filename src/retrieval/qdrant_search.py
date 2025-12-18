from typing import List
from src.db.qdrant_client import qdrant_service
from src.models.retrieved_context import RetrievedContext
from src.utils.logging import get_logger
from src.exceptions import QdrantSearchException

logger = get_logger(__name__)


class QdrantSearchService:
    """
    Service for performing search operations in Qdrant
    This layer provides search-specific functionality on top of the base Qdrant client
    """
    def __init__(self):
        self.qdrant_service = qdrant_service

    def search_by_text(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.3
    ) -> List[RetrievedContext]:
        """
        Search for documents relevant to the query text
        Note: This method assumes that query embedding is handled elsewhere
        """
        try:
            logger.info(f"Performing text-based search for query: {query[:50]}...")

            # In a real implementation, you would convert the query text to an embedding
            # using the same model that was used for the stored documents
            # For now, I'll use a placeholder embedding
            query_embedding = self._get_query_embedding(query)

            # Perform the search in Qdrant
            results = self.qdrant_service.search(
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold
            )

            logger.info(f"Found {len(results)} results for query")
            return results

        except Exception as e:
            logger.error(f"Error in Qdrant text search: {str(e)}")
            raise QdrantSearchException(f"Qdrant search failed: {str(e)}")

    def search_by_embedding(
        self,
        query_embedding: List[float],
        limit: int = 5,
        score_threshold: float = 0.3
    ) -> List[RetrievedContext]:
        """
        Search for documents using a pre-computed embedding vector
        """
        try:
            logger.info(f"Performing embedding-based search with vector of length {len(query_embedding)}")

            # Perform the search in Qdrant
            results = self.qdrant_service.search(
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold
            )

            logger.info(f"Found {len(results)} results for embedding query")
            return results

        except Exception as e:
            logger.error(f"Error in Qdrant embedding search: {str(e)}")
            raise QdrantSearchException(f"Qdrant embedding search failed: {str(e)}")

    def _get_query_embedding(self, query: str) -> List[float]:
        """
        Convert query text to embedding vector
        This is a placeholder - in production, use the same embedding model
        that was used for the stored documents
        """
        # Placeholder embedding generation
        # In a real implementation, you would use the same embedding model
        # that was used to create the embeddings stored in Qdrant
        placeholder_vector = [hash(c) % 1000 / 1000.0 for c in query[:100]]
        # Ensure the vector has the right dimension (pad or truncate as needed)
        target_dim = 1536
        if len(placeholder_vector) < target_dim:
            placeholder_vector.extend([0.0] * (target_dim - len(placeholder_vector)))
        else:
            placeholder_vector = placeholder_vector[:target_dim]

        return placeholder_vector

    def validate_connection(self) -> bool:
        """
        Validate that the Qdrant connection is working properly
        """
        try:
            return self.qdrant_service.check_connection()
        except Exception as e:
            logger.error(f"Qdrant connection validation failed: {str(e)}")
            return False


# Global instance
qdrant_search_service = QdrantSearchService()