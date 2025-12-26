from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from fastapi.responses import StreamingResponse
import json
import asyncio

router = APIRouter()

class StreamingAskRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

@router.post("/ask-streaming")
async def ask_streaming_endpoint(request: StreamingAskRequest):
    """Streaming endpoint that returns responses as they are generated"""
    try:
        # Generate a new session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Import here to avoid circular dependencies
        from services.generator import generate_answer

        async def event_generator():
            try:
                # Generate answer using RAG pipeline
                answer, citations = await generate_answer(
                    question=request.question,
                    session_id=session_id,
                    mode="global"
                )

                # Stream the response in chunks to simulate real-time streaming
                # Split the answer into sentences or phrases for more natural streaming
                import re
                # Split by sentence endings to create more natural chunks
                sentences = re.split(r'(?<=[.!?])\s+', answer)

                full_response = ""
                for sentence in sentences:
                    if sentence.strip():
                        full_response += sentence + " "
                        yield f"data: {json.dumps({'event': 'chunk', 'data': sentence.strip() + ' '})}\n\n"
                        # Small delay to simulate real streaming
                        await asyncio.sleep(0.05)

                # Send final message with citations and session info
                yield f"data: {json.dumps({'event': 'complete', 'data': {'citations': citations, 'session_id': session_id, 'final_answer': answer}})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'event': 'error', 'data': str(e)})}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except Exception as e:
        # For other exceptions, also provide more detailed information
        import traceback
        error_details = f"Exception: {str(e)}\nType: {type(e).__name__}\nTraceback: {traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_details)