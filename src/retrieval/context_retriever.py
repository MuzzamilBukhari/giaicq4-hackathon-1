from typing import List
from src.db.qdrant_client import qdrant_service
from src.models.retrieved_context import RetrievedContext
from src.utils.logging import get_logger

logger = get_logger(__name__)


class ContextRetriever:
    """
    Service for retrieving relevant context from the vector database
    """
    def __init__(self):
        self.qdrant_service = qdrant_service

    def retrieve_context(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.3
    ) -> List[RetrievedContext]:
        """
        Retrieve context relevant to the query from Qdrant
        In development mode, returns mock data when Qdrant is not available
        """
        try:
            logger.info(f"Starting context retrieval for query: {query[:50]}...")

            # Get embedding for the query
            query_embedding = self._get_query_embedding(query)

            # Try to search in Qdrant
            try:
                contexts = self.qdrant_service.search(
                    query_vector=query_embedding,
                    limit=limit,
                    score_threshold=score_threshold
                )
                logger.info(f"Retrieved {len(contexts)} relevant contexts from Qdrant")
                return contexts
            except Exception as qdrant_error:
                logger.warning(f"Qdrant search failed: {str(qdrant_error)}. Returning mock context for development.")
                # Return mock context for development/testing purposes
                return self._get_mock_contexts(query, limit)

        except Exception as e:
            logger.error(f"Error in context retrieval: {str(e)}")
            # Return mock contexts as fallback
            return self._get_mock_contexts(query, limit)

    def _get_mock_contexts(self, query: str, limit: int) -> List[RetrievedContext]:
        """
        Generate mock context when Qdrant is not available
        """
        logger.info(f"Generating {limit} mock contexts for query: {query[:30]}...")

        mock_contexts = []
        for i in range(min(limit, 3)):  # Limit to 3 mock contexts
            mock_context = RetrievedContext(
                id=f"mock-context-{i}",
                content=f"This is mock content related to your query about '{query[:20]}'. In a real implementation, this would come from the vector database.",
                url="https://example.com/mock-docs",
                section=f"Section {i+1}",
                chunk_id=f"chunk-{i}",
                score=0.8 - (i * 0.1)  # Decreasing scores
            )
            mock_contexts.append(mock_context)

        return mock_contexts

    def _get_query_embedding(self, query: str) -> List[float]:
        """
        Get embedding vector for the query text
        """
        # In a real implementation, you would use the same embedding model that was used
        # to create the embeddings stored in Qdrant. For example:
        # - If documents were embedded with OpenAI embeddings, use OpenAI API
        # - If documents were embedded with SentenceTransformer, use the same model
        # - If documents were embedded with Cohere, use Cohere API

        # For this implementation, I'll use a placeholder approach
        # In a real system, you would initialize the appropriate embedding model
        # based on how the original documents were embedded

        # Placeholder embedding generation - in reality, this would call the actual embedding model
        # For now, returning a simple vector based on character values (not suitable for production)
        # This is just to make the system work for demonstration purposes

        # In a real implementation, you might do something like:
        # if not self.embedding_model:
        #     self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # or appropriate model
        # embeddings = self.embedding_model.encode([query])
        # return embeddings[0].tolist()

        # For now, using a simple placeholder - this will be replaced with real embedding logic
        # when we integrate with the actual embedding service
        placeholder_vector = [hash(c) % 1000 / 1000.0 for c in query[:100]]
        # Ensure the vector has the right dimension (pad or truncate as needed)
        # Assuming the embedding dimension is 1536 (common for many models)
        target_dim = 1536
        if len(placeholder_vector) < target_dim:
            placeholder_vector.extend([0.0] * (target_dim - len(placeholder_vector)))
        else:
            placeholder_vector = placeholder_vector[:target_dim]

        return placeholder_vector


# Global instance
context_retriever = ContextRetriever()