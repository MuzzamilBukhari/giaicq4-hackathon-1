#!/usr/bin/env python3
"""
Database initialization script for the RAG Chatbot system.
Creates the necessary tables in the database including auth tables.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_db():
    # Import the main database connection and Base to get all models
    from db.connection import engine, Base
    from db.models import Session, Message    # Import existing models to register them

    print("Initializing database tables...")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()