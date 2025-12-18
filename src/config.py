from pydantic_settings import BaseSettings
from typing import List
import json
import os


class Settings(BaseSettings):
    # Qdrant Configuration
    qdrant_url: str = "your_qdrant_cluster_url"
    qdrant_api_key: str = "your_qdrant_api_key"
    qdrant_collection_name: str = "book-content"  # Default value, can be overridden by env var

    # Google Gemini Configuration
    google_api_key: str = "your_google_api_key"
    gemini_model: str = "gemini-1.5-pro"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"

    # Application Configuration
    cors_origins: List[str] = ["http://localhost:3000", "https://your-docusaurus-site.com"]
    log_level: str = "info"

    # Production Configuration
    debug: bool = False
    environment: str = "development"  # development, staging, production
    max_request_size: int = 10 * 1024 * 1024  # 10MB in bytes
    request_timeout: int = 30  # seconds
    max_context_chunks: int = 10
    response_streaming_timeout: int = 60  # seconds
    rate_limit_requests: int = 100  # per minute per IP
    rate_limit_window: int = 60  # seconds

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from existing .env

    @classmethod
    def parse_cors_origins(cls, cors_origins_str: str) -> List[str]:
        """Parse CORS origins from environment variable string."""
        try:
            return json.loads(cors_origins_str)
        except json.JSONDecodeError:
            return ["http://localhost:3000"]


# Create settings instance
settings = Settings()

# Override cors_origins from environment if present
cors_env = os.getenv("CORS_ORIGINS")
if cors_env:
    settings.cors_origins = Settings.parse_cors_origins(cors_env)