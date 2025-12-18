from typing import List, Dict, Any
from src.db.qdrant_client import qdrant_service
from src.llm.gemini_client import gemini_service
from src.retrieval.context_retriever import context_retriever
from src.llm.response_generator import response_generator
from src.models.query_request import QueryRequest
from src.models.retrieved_context import RetrievedContext
from src.models.response import ChatResponse, Source, TokenUsage
from src.exceptions import QdrantSearchException, GeminiGenerationException
from src.utils.validation import sanitize_input
from src.utils.logging import get_logger
from uuid import uuid4
from datetime import datetime
import json

logger = get_logger(__name__)


class RAGService:
    """
    Core service for RAG (Retrieval-Augmented Generation) functionality
    Handles the complete flow from query to response
    """
    def __init__(self):
        self.qdrant_service = qdrant_service
        self.gemini_service = gemini_service
        self.context_retriever = context_retriever
        self.response_generator = response_generator

    def process_query(
        self,
        query_request: QueryRequest
    ) -> ChatResponse:
        """
        Process a user query through the complete RAG pipeline
        """
        try:
            # Sanitize the input query
            sanitized_query = sanitize_input(query_request.query)

            # Validate query length
            if len(sanitized_query) < 1 or len(sanitized_query) > 2000:
                raise ValueError("Query must be between 1 and 2000 characters")

            # Retrieve relevant context from Qdrant using the context retriever
            retrieved_contexts = self.context_retriever.retrieve_context(sanitized_query)

            # If no contexts are retrieved, try a fallback approach
            if not retrieved_contexts:
                logger.warning(f"No contexts retrieved for query: {sanitized_query[:50]}...")
                # Still attempt to generate a response without context
                response_text, token_usage = self.response_generator.generate_response(
                    query=sanitized_query,
                    contexts=None  # No contexts available
                )
            else:
                # Generate response using the response generator
                response_text, token_usage = self.response_generator.generate_response(
                    query=sanitized_query,
                    contexts=retrieved_contexts
                )

            # Validate response quality
            is_quality_response = self.response_generator.validate_response_quality(
                response_text,
                sanitized_query,
                retrieved_contexts if retrieved_contexts else None
            )

            if not is_quality_response:
                logger.warning(f"Response quality check failed for query: {sanitized_query[:50]}...")
                # For now, we'll still return the response but log the quality issue
                # In production, you might want to handle this differently

            # Create response object with sources
            response = self._create_response_object(
                response_text,
                retrieved_contexts if retrieved_contexts else [],
                query_request,
                token_usage
            )

            logger.info(f"Successfully processed query: {sanitized_query[:50]}...")
            return response

        except QdrantSearchException as e:
            logger.error(f"Qdrant search error: {str(e)}")
            # Fallback: try to generate response without context
            try:
                response_text, token_usage = self.response_generator.generate_response(
                    query=sanitize_input(query_request.query),
                    contexts=None
                )
                return self._create_response_object(
                    response_text,
                    [],
                    query_request,
                    token_usage
                )
            except Exception:
                raise
        except GeminiGenerationException as e:
            logger.error(f"Gemini generation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing query: {str(e)}")
            raise

    def retrieve_context(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.3
    ) -> List[RetrievedContext]:
        """
        Retrieve relevant context from Qdrant based on the query
        """
        try:
            logger.info(f"Retrieving context for query: {query[:50]}...")

            # Use the context retriever service
            contexts = self.context_retriever.retrieve_context(
                query=query,
                limit=limit,
                score_threshold=score_threshold
            )

            logger.info(f"Retrieved {len(contexts)} context items")
            return contexts

        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise QdrantSearchException(f"Failed to retrieve context: {str(e)}")

    def _format_context_for_gemini(
        self,
        retrieved_contexts: List[RetrievedContext]
    ) -> List[Dict[str, Any]]:
        """
        Format retrieved contexts for use with Gemini
        """
        formatted_context = []
        for context in retrieved_contexts:
            formatted_context.append({
                'content': context.content,
                'url': context.url,
                'section': context.section,
                'score': context.score
            })

        return formatted_context

    def _generate_response_with_gemini(
        self,
        query: str,
        context: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a response using Gemini with the provided context
        """
        try:
            response_text = self.gemini_service.generate_response(
                prompt=query,
                context=context,
                stream=False
            )

            logger.info("Successfully generated response from Gemini")
            return response_text

        except Exception as e:
            logger.error(f"Error generating response with Gemini: {str(e)}")
            raise GeminiGenerationException(f"Failed to generate response: {str(e)}")

    def _create_response_object(
        self,
        response_text: str,
        retrieved_contexts: List[RetrievedContext],
        original_request: QueryRequest,
        token_usage = None
    ) -> ChatResponse:
        """
        Create a ChatResponse object from the generated response and context
        """
        # Convert RetrievedContext objects to Source objects
        sources = []
        for context in retrieved_contexts:
            source = Source(
                url=context.url,
                section=context.section,
                relevance_score=context.score
            )
            sources.append(source)

        # Create the response object
        response = ChatResponse(
            id=str(uuid4()),
            answer=response_text,
            sources=sources,
            created_at=datetime.now().isoformat(),
            model=self.gemini_service.model,
            usage=token_usage  # Token usage from the response generator
        )

        return response

    def process_query_streaming(
        self,
        query_request: QueryRequest
    ) -> Any:  # Generator for streaming
        """
        Process a user query with streaming response
        """
        try:
            # Sanitize the input query
            sanitized_query = sanitize_input(query_request.query)

            # Retrieve relevant context from Qdrant using the context retriever
            retrieved_contexts = self.context_retriever.retrieve_context(sanitized_query)

            # Generate streaming response using the response generator
            stream = self.response_generator.generate_response_streaming(
                query=sanitized_query,
                contexts=retrieved_contexts
            )

            return stream

        except Exception as e:
            logger.error(f"Error in streaming query processing: {str(e)}")
            raise


# Global instance
rag_service = RAGService()