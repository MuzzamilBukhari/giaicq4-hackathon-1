from pydantic_settings import Settings as PydanticSettings
from typing import Optional


class Settings(PydanticSettings):
    # Qdrant configuration
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "textbook_chunks"

    # Neon Postgres configuration
    neon_db_url: str = "postgresql://postgres:postgres@localhost:5432/rag_chatbot"

    # OpenAI/ChatKit configuration
    openai_api_key: str
    chatkit_api_key: Optional[str] = None

    # Application settings
    app_name: str = "RAG Chatbot"
    debug: bool = False
    allowed_origins: str = "http://localhost:3000,http://localhost:3001,https://yourdomain.com"

    class Config:
        env_file = ".env"


# Create a global settings instance
settings = Settings()