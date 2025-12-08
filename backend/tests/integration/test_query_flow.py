"""
Integration tests for the query flow with sample data
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.mark.asyncio
async def test_query_endpoint_basic():
    """Test basic query functionality with mock data"""
    with patch('app.agent.chatkit_agent') as mock_agent:
        # Mock the agent response
        mock_agent.generate_answer_with_citations.return_value = {
            "answer": "This is a test answer based on the context.",
            "sources": [
                {
                    "doc_path": "/test/doc.md",
                    "heading": "Test Heading",
                    "excerpt": "This is a test excerpt.",
                    "score": 0.85
                }
            ],
            "meta": {
                "latency_ms": 100,
                "model": "test-model",
                "retrieval_count": 1
            }
        }

        with TestClient(app) as client:
            response = client.post(
                "/query",
                json={"question": "What is this?"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data
            assert "meta" in data
            assert data["answer"] == "This is a test answer based on the context."


@pytest.mark.asyncio
async def test_selected_text_endpoint():
    """Test selected text endpoint with mock data"""
    with patch('app.agent.chatkit_agent') as mock_agent:
        # Mock the agent response
        mock_agent.generate_answer_with_citations.return_value = {
            "answer": "This is a test answer based on selected text.",
            "sources": [],
            "meta": {
                "latency_ms": 50,
                "model": "test-model",
                "retrieval_count": 0
            }
        }

        with TestClient(app) as client:
            response = client.post(
                "/selected",
                json={
                    "question": "Explain this",
                    "selected_text": "This is the selected text."
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert data["answer"] == "This is a test answer based on selected text."


def test_health_check():
    """Test the health check endpoint"""
    with TestClient(app) as client:
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "app_version" in data