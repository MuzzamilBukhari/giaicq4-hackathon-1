from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Generator
from src.models.query_request import QueryRequest
from src.models.response import ChatResponse
from src.services.rag_service import rag_service
from src.exceptions import query_validation_error, internal_error
from src.utils.validation import validate_query_length, is_safe_content
from src.utils.logging import get_logger
from uuid import uuid4
import json

logger = get_logger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(query_request: QueryRequest):
    """
    Process a user query and return a RAG-generated response
    """
    request_id = str(uuid4())
    logger.info(f"[{request_id}] Received chat request: {query_request.query[:50]}...")

    try:
        # Additional validation beyond Pydantic model validation
        if not validate_query_length(query_request.query):
            logger.warning(f"[{request_id}] Query validation failed: length check")
            raise query_validation_error("Query must be between 1 and 2000 characters")

        # Validate that query doesn't contain harmful content
        if not is_safe_content(query_request.query):
            logger.warning(f"[{request_id}] Query validation failed: safety check")
            raise query_validation_error("Query contains potentially harmful content")

        logger.debug(f"[{request_id}] Starting RAG processing")

        # Process the query through the RAG service
        response = rag_service.process_query(query_request)

        logger.info(f"[{request_id}] Successfully processed chat request")
        logger.debug(f"[{request_id}] Response sources count: {len(response.sources)}")

        # Return with proper headers for frontend compatibility
        return JSONResponse(
            content=response.dict(),
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Headers": "content-type",
                "X-Request-ID": request_id,  # Include request ID for debugging
            }
        )
    except HTTPException as e:
        logger.error(f"[{request_id}] HTTP error in chat endpoint: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"[{request_id}] Error in chat endpoint: {str(e)}")
        raise internal_error(f"Error processing query: {str(e)}")


@router.post("/chat/stream")
async def chat_stream_endpoint(query_request: QueryRequest):
    """
    Process a user query and stream the RAG-generated response
    """
    try:
        logger.info(f"Received streaming chat request: {query_request.query[:50]}...")

        # Additional validation
        if not validate_query_length(query_request.query):
            raise query_validation_error("Query must be between 1 and 2000 characters")

        # Validate that query doesn't contain harmful content
        if not is_safe_content(query_request.query):
            raise query_validation_error("Query contains potentially harmful content")

        async def generate_stream():
            try:
                # Process the query through the RAG service with streaming
                stream = rag_service.process_query_streaming(query_request)

                # Stream the response
                for chunk in stream:
                    yield f"data: {json.dumps({'content': chunk})}\n\n"

            except Exception as e:
                logger.error(f"Error in streaming response: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        logger.info("Starting streaming response")
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Headers": "content-type",
            }
        )

    except Exception as e:
        logger.error(f"Error in chat stream endpoint: {str(e)}")
        raise internal_error(f"Error processing streaming query: {str(e)}")


