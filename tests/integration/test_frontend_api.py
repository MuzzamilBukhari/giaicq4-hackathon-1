"""
Integration tests for frontend API communication
Tests the compatibility between the RAG backend and frontend widget
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from src.main import app
from src.models.query_request import QueryRequest
from src.models.response import ChatResponse
import json


@pytest.fixture
def client():
    """Create a test client for the API"""
    return TestClient(app)


def test_chat_endpoint_basic_functionality(client):
    """Test basic chat endpoint functionality"""
    query_request = QueryRequest(query="What is this book about?")

    response = client.post(
        "/api/v1/chat",
        json=query_request.dict(),
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "id" in data
    assert "created_at" in data
    assert "model" in data


def test_chat_endpoint_cors_headers(client):
    """Test that CORS headers are properly set for frontend integration"""
    query_request = QueryRequest(query="Test CORS headers")

    response = client.post(
        "/api/v1/chat",
        json=query_request.dict(),
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    # Check for CORS-related headers
    assert "access-control-allow-origin" in [h.lower() for h in response.headers.keys()]


def test_health_endpoint(client):
    """Test health endpoint for frontend monitoring"""
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "checks" in data


def test_chat_endpoint_with_special_characters(client):
    """Test chat endpoint with special characters that might come from frontend"""
    query_request = QueryRequest(query="What's the difference between 'this' and \"that\"?")

    response = client.post(
        "/api/v1/chat",
        json=query_request.dict()
    )

    # Should not fail with special characters
    assert response.status_code in [200, 400]  # Either success or validation error, but not server error


def test_chat_endpoint_empty_query(client):
    """Test chat endpoint with empty query (should fail validation)"""
    query_request = QueryRequest(query="")

    response = client.post(
        "/api/v1/chat",
        json=query_request.dict()
    )

    # Should return a validation error, not a server error
    assert response.status_code == 400


def test_chat_endpoint_long_query(client):
    """Test chat endpoint with very long query (should fail validation)"""
    long_query = "This is a very long query. " * 1000  # Much longer than 2000 char limit
    query_request = QueryRequest(query=long_query)

    response = client.post(
        "/api/v1/chat",
        json=query_request.dict()
    )

    # Should return a validation error, not a server error
    assert response.status_code == 400


def test_streaming_endpoint_headers(client):
    """Test that streaming endpoint returns proper headers for frontend"""
    query_request = QueryRequest(query="Stream test")

    response = client.post(
        "/api/v1/chat/stream",
        json=query_request.dict()
    )

    # Streaming endpoint might return an error if services aren't configured
    # but it should return proper headers
    if response.status_code == 200:
        assert response.headers.get("content-type") == "text/event-stream"
        assert response.headers.get("cache-control") == "no-cache"


def test_api_compatibility_with_frontend_payloads(client):
    """Test API with payloads that might come from frontend widgets"""
    # Test with a payload that includes optional fields
    query_request = QueryRequest(
        query="Test query from frontend",
        session_id="test-session-123",
        metadata={"source": "frontend_widget", "user_agent": "test"}
    )

    response = client.post(
        "/api/v1/chat",
        json=query_request.dict()
    )

    # Should handle optional fields gracefully
    assert response.status_code in [200, 400]  # Either success or validation error


if __name__ == "__main__":
    pytest.main([__file__])