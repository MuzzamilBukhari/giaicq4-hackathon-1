"""
Unit tests for RAG service
Tests the core functionality of the RAG system
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.rag_service import RAGService
from src.models.query_request import QueryRequest
from src.models.retrieved_context import RetrievedContext
from src.exceptions import QdrantSearchException, GeminiGenerationException


class TestRAGService:
    def setup_method(self):
        """Setup test fixtures before each test method."""
        self.rag_service = RAGService()
        # Mock the dependencies
        self.rag_service.context_retriever = Mock()
        self.rag_service.response_generator = Mock()
        self.rag_service.gemini_service = Mock()

    def test_process_query_success(self):
        """Test successful query processing"""
        # Arrange
        query_request = QueryRequest(query="What is Python?")
        mock_context = [RetrievedContext(
            id="1",
            content="Python is a programming language",
            url="https://example.com",
            section="Introduction",
            chunk_id="chunk-1",
            score=0.8
        )]
        mock_response_text = "Python is a high-level programming language"
        mock_token_usage = Mock()

        self.rag_service.context_retriever.retrieve_context.return_value = mock_context
        self.rag_service.response_generator.generate_response.return_value = (mock_response_text, mock_token_usage)
        self.rag_service.response_generator.validate_response_quality.return_value = True

        # Act
        result = self.rag_service.process_query(query_request)

        # Assert
        assert result.answer == mock_response_text
        assert len(result.sources) == 1
        assert result.sources[0].url == "https://example.com"
        assert result.usage == mock_token_usage

    def test_process_query_no_context(self):
        """Test query processing when no context is retrieved"""
        # Arrange
        query_request = QueryRequest(query="What is Python?")
        mock_response_text = "Python is a high-level programming language"
        mock_token_usage = Mock()

        self.rag_service.context_retriever.retrieve_context.return_value = []
        self.rag_service.response_generator.generate_response.return_value = (mock_response_text, mock_token_usage)
        self.rag_service.response_generator.validate_response_quality.return_value = True

        # Act
        result = self.rag_service.process_query(query_request)

        # Assert
        assert result.answer == mock_response_text
        assert len(result.sources) == 0
        assert result.usage == mock_token_usage

    def test_process_query_qdrant_error_with_fallback(self):
        """Test fallback when Qdrant search fails"""
        # Arrange
        query_request = QueryRequest(query="What is Python?")
        mock_response_text = "Python is a high-level programming language"
        mock_token_usage = Mock()

        self.rag_service.context_retriever.retrieve_context.side_effect = QdrantSearchException("Search failed")
        self.rag_service.response_generator.generate_response.return_value = (mock_response_text, mock_token_usage)
        self.rag_service.response_generator.validate_response_quality.return_value = True

        # Act
        result = self.rag_service.process_query(query_request)

        # Assert - should fallback to generating response without context
        assert result.answer == mock_response_text
        assert len(result.sources) == 0  # No sources when using fallback

    def test_process_query_qdrant_error_fallback_also_fails(self):
        """Test when both Qdrant and fallback fail"""
        # Arrange
        query_request = QueryRequest(query="What is Python?")

        self.rag_service.context_retriever.retrieve_context.side_effect = QdrantSearchException("Search failed")
        self.rag_service.response_generator.generate_response.side_effect = GeminiGenerationException("Generation failed")

        # Act & Assert
        with pytest.raises(GeminiGenerationException):
            self.rag_service.process_query(query_request)

    def test_process_query_gemini_error(self):
        """Test when Gemini generation fails"""
        # Arrange
        query_request = QueryRequest(query="What is Python?")
        mock_context = [RetrievedContext(
            id="1",
            content="Python is a programming language",
            url="https://example.com",
            section="Introduction",
            chunk_id="chunk-1",
            score=0.8
        )]

        self.rag_service.context_retriever.retrieve_context.return_value = mock_context
        self.rag_service.response_generator.generate_response.side_effect = GeminiGenerationException("Generation failed")

        # Act & Assert
        with pytest.raises(GeminiGenerationException):
            self.rag_service.process_query(query_request)

    def test_retrieve_context_success(self):
        """Test successful context retrieval"""
        # Arrange
        query = "Python programming"
        mock_context = [RetrievedContext(
            id="1",
            content="Python is a programming language",
            url="https://example.com",
            section="Introduction",
            chunk_id="chunk-1",
            score=0.8
        )]

        self.rag_service.context_retriever.retrieve_context.return_value = mock_context

        # Act
        result = self.rag_service.retrieve_context(query)

        # Assert
        assert result == mock_context
        self.rag_service.context_retriever.retrieve_context.assert_called_once_with(
            query=query, limit=5, score_threshold=0.3
        )

    def test_process_query_with_long_query(self):
        """Test that very long queries are handled properly"""
        # Arrange
        long_query = "This is a very long query " * 100  # Exceeds normal length
        query_request = QueryRequest(query=long_query)

        # Act & Assert
        with pytest.raises(ValueError):
            self.rag_service.process_query(query_request)

    def test_process_query_with_empty_query(self):
        """Test that empty queries are handled properly"""
        # Arrange
        query_request = QueryRequest(query="")

        # Act & Assert
        with pytest.raises(ValueError):
            self.rag_service.process_query(query_request)


if __name__ == "__main__":
    pytest.main([__file__])