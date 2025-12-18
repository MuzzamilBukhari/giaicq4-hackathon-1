from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
import re


class QueryRequest(BaseModel):
    """
    Represents a user's natural language question submitted to the RAG system
    """
    query: str = Field(
        ...,
        description="The user's question or prompt",
        min_length=1,
        max_length=2000
    )
    session_id: Optional[str] = Field(
        None,
        description="Identifier for conversation context",
        pattern=r"^[a-zA-Z0-9_-]+$"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional request metadata"
    )

    @validator('query')
    def validate_query_content(cls, v):
        """
        Validate that query doesn't contain harmful content patterns
        """
        # Basic check for potentially harmful patterns
        harmful_patterns = [
            r'<script',  # XSS attempts
            r'javascript:',  # JavaScript injection
            r'vbscript:',  # VBScript injection
            r'on\w+\s*=',  # Event handlers
        ]

        for pattern in harmful_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Query contains potentially harmful content')

        return v

    @validator('session_id')
    def validate_session_id(cls, v):
        """
        Validate session_id format if provided
        """
        if v is not None:
            # Basic UUID-like pattern check
            if not re.match(r'^[a-zA-Z0-9_-]+$', v):
                raise ValueError('Session ID must contain only alphanumeric characters, hyphens, and underscores')
        return v