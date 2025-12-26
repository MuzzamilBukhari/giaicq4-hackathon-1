#!/usr/bin/env python3
"""
Simple database initialization script for the RAG Chatbot system.
Creates the necessary tables in the database.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def init_db():
    # Import the database models and engine
    from db.models import engine, Base, Session, Message

    print("Initializing database tables...")

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())