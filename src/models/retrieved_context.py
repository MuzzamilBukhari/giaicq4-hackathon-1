from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime


class RetrievedContext(BaseModel):
    """
    Represents relevant document segments retrieved from Qdrant embeddings
    """
    id: str = Field(
        ...,
        description="Unique identifier for the document chunk"
    )
    content: str = Field(
        ...,
        description="The actual text content that matches the query"
    )
    url: str = Field(
        ...,
        description="Source URL of the documentation page"
    )
    section: str = Field(
        ...,
        description="Section title or heading from the source"
    )
    chunk_id: str = Field(
        ...,
        description="Identifier for this specific chunk"
    )
    score: float = Field(
        ...,
        description="Similarity score from vector search (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    @validator('url')
    def validate_url(cls, v):
        """
        Validate URL format
        """
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(v):
            raise ValueError('URL must be valid format')
        return v

    @validator('score')
    def validate_score(cls, v):
        """
        Validate score is between 0.0 and 1.0
        """
        if not 0.0 <= v <= 1.0:
            raise ValueError('Score must be between 0.0 and 1.0')
        return v