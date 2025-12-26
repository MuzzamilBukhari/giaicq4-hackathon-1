import cohere
import os
from typing import List, Tuple, Dict, Any
from pydantic import BaseModel


class CohereProvider:
    """
    Provider class for Cohere API interactions including embeddings and text generation.
    """

    def __init__(self):
        """
        Initialize the Cohere client with API key from environment variables.
        """
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(api_key)

    def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text using Cohere's chat API.

        Args:
            prompt: The input prompt for text generation
            max_tokens: Maximum number of tokens to generate

        Returns:
            Generated text response
        """
        try:
            response = self.client.chat(
                message=prompt,
                model="command-r-plus-08-2024",  # Using a specific version of the model
                max_tokens=max_tokens,
                temperature=0.7,
            )

            if response.text:
                return response.text
            else:
                return "I couldn't generate a response based on the provided context."

        except Exception as e:
            print(f"Error generating text with Cohere: {e}")
            raise

    def generate_text_streaming(self, prompt: str, max_tokens: int = 500):
        """
        Generate text using Cohere's chat API with streaming support.

        Args:
            prompt: The input prompt for text generation
            max_tokens: Maximum number of tokens to generate

        Returns:
            Generator that yields text chunks
        """
        try:
            response = self.client.chat_stream(
                message=prompt,
                model="command-r-plus-08-2024",  # Using a specific version of the model
                max_tokens=max_tokens,
                temperature=0.7,
            )

            for event in response:
                if event.event_type == "text-generation":
                    yield event.text
                elif event.event_type == "stream-end":
                    break

        except Exception as e:
            print(f"Error generating text with Cohere streaming: {e}")
            raise

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for the given text using Cohere's embedding API.

        Args:
            text: The input text to embed

        Returns:
            List of embedding values
        """
        try:
            response = self.client.embed(
                texts=[text],
                model="embed-english-v3.0",  # Cohere's latest embedding model
                input_type="search_document"  # Optimize for document search
            )

            if response.embeddings:
                return response.embeddings[0]
            else:
                raise ValueError("No embeddings returned from Cohere API")

        except Exception as e:
            print(f"Error generating embedding with Cohere: {e}")
            raise

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts using Cohere's embedding API.

        Args:
            texts: List of input texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            response = self.client.embed(
                texts=texts,
                model="embed-english-v3.0",  # Cohere's latest embedding model
                input_type="search_document"  # Optimize for document search
            )

            if response.embeddings:
                return response.embeddings
            else:
                raise ValueError("No embeddings returned from Cohere API")

        except Exception as e:
            print(f"Error generating embeddings with Cohere: {e}")
            raise