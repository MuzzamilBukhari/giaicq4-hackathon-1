from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

class AskSelectedRequest(BaseModel):
    question: str
    selected_text: str
    session_id: Optional[str] = None

class AskSelectedResponse(BaseModel):
    answer: str
    citations: list
    session_id: str

@router.post("/ask-selected", response_model=AskSelectedResponse)
async def ask_selected_endpoint(request: AskSelectedRequest):
    try:
        # Generate a new session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Import here to avoid circular dependencies
        from services.generator import generate_answer
        from services.session_logger import log_message

        # Generate answer using selected text only (no retrieval)
        answer, citations = await generate_answer(
            question=request.question,
            selected_text=request.selected_text,
            session_id=session_id,
            mode="selected"
        )

        # Log the interaction
        await log_message(session_id, "user", f"Question: {request.question}\nSelected: {request.selected_text}")
        await log_message(session_id, "ai", answer)

        return AskSelectedResponse(
            answer=answer,
            citations=citations,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))