from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import os
from datetime import datetime
from typing import List, Dict, Any

# Async database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to messages
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    sender = Column(String)  # 'user' or 'ai'
    text = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to session
    session = relationship("Session", back_populates="messages")

# Create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Database operations
async def create_session(session_id: str):
    async with AsyncSessionLocal() as db:
        session = Session(id=session_id)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

async def create_message(session_id: str, sender: str, text: str):
    async with AsyncSessionLocal() as db:
        # Check if session exists, create if not
        from sqlalchemy import select
        result = await db.execute(select(Session).filter(Session.id == session_id))
        session = result.scalars().first()
        if not session:
            await create_session(session_id)

        message = Message(session_id=session_id, sender=sender, text=text)
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

async def get_conversation_history(session_id: str) -> List[Dict[str, Any]]:
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        result = await db.execute(
            select(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.timestamp)
        )
        messages = result.scalars().all()

        # Convert to dict format for response
        message_list = []
        for msg in messages:
            message_list.append({
                "id": str(msg.id),
                "session_id": msg.session_id,
                "sender": msg.sender,
                "text": msg.text,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
            })

        return message_list

async def get_session_id() -> str:
    """
    Helper function to get or create a session ID.
    """
    import uuid
    return str(uuid.uuid4())