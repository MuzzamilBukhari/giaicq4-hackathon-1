from openai import OpenAI
from typing import List, Dict, Any, Generator
from src.config import settings
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service class for interacting with Google Gemini via OpenAI-compatible endpoint
    """
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.google_api_key,
            base_url=settings.gemini_base_url
        )
        self.model = settings.gemini_model

    def generate_response(
        self,
        prompt: str,
        context: List[Dict[str, Any]] = None,
        stream: bool = False
    ) -> str:
        """
        Generate a response from Gemini based on the prompt and context
        """
        try:
            # Prepare the messages for the chat completion
            messages = []

            # Add system message with context if provided
            if context:
                context_str = "\n\nRelevant context:\n"
                for item in context:
                    context_str += f"- {item.get('section', 'Section')}: {item.get('content', '')}\n"
                    if 'url' in item:
                        context_str += f"  Source: {item['url']}\n"

                messages.append({
                    "role": "system",
                    "content": f"You are a helpful assistant that answers questions based on the provided documentation. Use the following context to answer the user's question:\n{context_str}\n\nWhen providing answers, please cite the relevant sources when possible."
                })
            else:
                messages.append({
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on documentation. Provide accurate and helpful responses."
                })

            # Add the user's query
            messages.append({
                "role": "user",
                "content": prompt
            })

            # Call the OpenAI-compatible Gemini API with parameters supported by Google's API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more factual, consistent responses
                max_tokens=1500,  # Increased to allow for more comprehensive answers
                stream=stream
            )

            if stream:
                # For streaming, return the response object
                return response
            else:
                # For non-streaming, return the content
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating response from Gemini: {str(e)}")
            raise

    def stream_response(
        self,
        prompt: str,
        context: List[Dict[str, Any]] = None
    ) -> Generator[str, None, None]:
        """
        Stream response tokens from Gemini
        """
        try:
            # Prepare the messages for the chat completion
            messages = []

            # Add system message with context if provided
            if context:
                context_str = "\n\nRelevant context:\n"
                for item in context:
                    context_str += f"- {item.get('section', 'Section')}: {item.get('content', '')}\n"
                    if 'url' in item:
                        context_str += f"  Source: {item['url']}\n"

                messages.append({
                    "role": "system",
                    "content": f"You are a helpful assistant that answers questions based on the provided documentation. Use the following context to answer the user's question:\n{context_str}\n\nWhen providing answers, please cite the relevant sources when possible."
                })
            else:
                messages.append({
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on documentation. Provide accurate and helpful responses."
                })

            # Add the user's query
            messages.append({
                "role": "user",
                "content": prompt
            })

            # Call the OpenAI-compatible Gemini API with streaming and parameters supported by Google's API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more factual, consistent responses
                max_tokens=1500,  # Increased to allow for more comprehensive answers
                stream=True
            )

            # Yield each token as it arrives
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Error streaming response from Gemini: {str(e)}")
            raise

    def check_connection(self) -> bool:
        """
        Check if the Gemini connection is working by making a simple request
        """
        try:
            response = self.generate_response("Test connection", stream=False)
            return bool(response and len(response) > 0)
        except Exception as e:
            logger.error(f"Gemini connection failed: {str(e)}")
            return False


# Global instance
gemini_service = GeminiService()