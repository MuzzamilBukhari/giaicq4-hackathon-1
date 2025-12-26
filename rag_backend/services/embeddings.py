import os
from typing import List
from .cohere_provider import CohereProvider

async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for the given text using Cohere embedding model.
    """
    try:
        cohere_provider = CohereProvider()
        embedding = await cohere_provider.generate_embedding(text)
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise

async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts.
    """
    try:
        cohere_provider = CohereProvider()
        embeddings = await cohere_provider.generate_embeddings(texts)
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise