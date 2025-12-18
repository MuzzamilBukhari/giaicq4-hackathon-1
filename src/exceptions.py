from typing import Optional
from fastapi import HTTPException, status


class RAGException(Exception):
    """
    Base exception class for RAG-related errors
    """
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class QueryValidationException(RAGException):
    """
    Exception raised for query validation errors
    """
    pass


class QdrantConnectionException(RAGException):
    """
    Exception raised when there's an issue connecting to Qdrant
    """
    pass


class QdrantSearchException(RAGException):
    """
    Exception raised when there's an issue with Qdrant search
    """
    pass


class GeminiConnectionException(RAGException):
    """
    Exception raised when there's an issue connecting to Gemini
    """
    pass


class GeminiGenerationException(RAGException):
    """
    Exception raised when there's an issue generating response from Gemini
    """
    pass


class ConfigurationException(RAGException):
    """
    Exception raised when there's an issue with application configuration
    """
    pass


def create_http_exception(
    status_code: int,
    detail: str,
    headers: Optional[dict] = None
) -> HTTPException:
    """
    Create an HTTPException with the given parameters
    """
    return HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers
    )


def query_validation_error(detail: str = "Invalid query format or content") -> HTTPException:
    """
    Create an HTTPException for query validation errors
    """
    return create_http_exception(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def internal_error(detail: str = "Internal server error during processing") -> HTTPException:
    """
    Create an HTTPException for internal server errors
    """
    return create_http_exception(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail
    )


def service_unavailable(detail: str = "Service temporarily unavailable") -> HTTPException:
    """
    Create an HTTPException for service unavailable errors
    """
    return create_http_exception(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=detail
    )


def too_many_requests(detail: str = "Rate limit exceeded") -> HTTPException:
    """
    Create an HTTPException for rate limiting
    """
    return create_http_exception(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=detail
    )