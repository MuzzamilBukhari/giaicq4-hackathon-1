from fastapi import APIRouter
from typing import Dict, Any
from src.db.qdrant_client import qdrant_service
from src.llm.gemini_client import gemini_service
from src.utils.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check for the entire RAG system
    """
    try:
        # Check Qdrant connection
        qdrant_healthy = qdrant_service.check_connection()

        # Check Gemini connection
        gemini_healthy = gemini_service.check_connection()

        # Overall health status
        overall_healthy = qdrant_healthy and gemini_healthy

        health_status = {
            "status": "healthy" if overall_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "qdrant_connection": qdrant_healthy,
                "gemini_connection": gemini_healthy,
                "api_server": True  # If we reach here, API server is running
            }
        }

        # Log the health check
        logger.info(f"Health check completed. Overall status: {health_status['status']}")

        return health_status

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "checks": {
                "qdrant_connection": False,
                "gemini_connection": False,
                "api_server": True
            }
        }


@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check to determine if the service is ready to accept traffic
    """
    try:
        # For readiness, we might have different criteria than health
        # For now, using the same checks as health
        qdrant_healthy = qdrant_service.check_connection()
        gemini_healthy = gemini_service.check_connection()

        ready = qdrant_healthy and gemini_healthy

        return {
            "status": "ready" if ready else "not_ready",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return {
            "status": "not_ready",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }