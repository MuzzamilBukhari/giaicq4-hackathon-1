from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Message(BaseModel):
    id: str
    session_id: str
    sender: str
    text: str
    timestamp: str

class HistoryResponse(BaseModel):
    messages: List[Message]

@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    try:
        # Import here to avoid circular dependencies
        from db.models import get_conversation_history

        # Get conversation history
        messages = await get_conversation_history(session_id)
        return HistoryResponse(messages=messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))