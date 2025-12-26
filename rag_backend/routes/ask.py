from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    citations: list
    session_id: str

@router.post("/ask", response_model=AskResponse)
async def ask_endpoint(request: AskRequest):
    try:
        # Generate a new session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Import here to avoid circular dependencies
        from services.generator import generate_answer
        # from services.session_logger import log_message  # Temporarily commented out

        # Generate answer using RAG pipeline
        answer, citations = await generate_answer(
            question=request.question,
            session_id=session_id,
            mode="global"
        )

        # Log the interaction - temporarily commented out due to DB connection issues
        # await log_message(session_id, "user", request.question)
        # await log_message(session_id, "ai", answer)

        return AskResponse(
            answer=answer,
            citations=citations,
            session_id=session_id
        )
    except ImportError as e:
        # This is likely the real error - capture and return it properly
        import traceback
        error_details = f"ImportError: {str(e)}\nTraceback: {traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_details)
    except Exception as e:
        # For other exceptions, also provide more detailed information
        import traceback
        error_details = f"Exception: {str(e)}\nType: {type(e).__name__}\nTraceback: {traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_details)