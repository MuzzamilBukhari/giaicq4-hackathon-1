from typing import Dict, List, Any, Optional
from .config import settings
from openai import OpenAI
import logging


class ChatKitAgent:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_answer_with_citations(
        self,
        question: str,
        retrieved_contexts: List[Dict[str, Any]],
        selected_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate an answer using ChatKit with proper citations
        """
        start_time = __import__('time').time()

        try:
            # Build the prompt based on whether we're using selected text only or retrieved context
            if selected_text:
                # Use only the selected text as context
                system_message = (
                    "You are an AI assistant that answers questions based on provided text. "
                    "Always provide answers that are grounded in the provided text. "
                    "If the text doesn't contain information to answer the question, say so explicitly. "
                    "Format your response with proper citations to the source."
                )

                user_message = f"Question: {question}\n\nSelected Text: {selected_text}"
            else:
                # Use retrieved context from the vector database
                system_message = (
                    "You are an AI assistant that answers questions based on provided textbook content. "
                    "Always provide answers that are grounded in the provided context. "
                    "Cite the specific sections where the information comes from. "
                    "If the context doesn't contain information to answer the question, say so explicitly. "
                    "Format your response with proper citations to the source documents."
                )

                # Format the retrieved contexts
                context_text = ""
                for i, ctx in enumerate(retrieved_contexts):
                    context_text += f"\n--- Context {i+1} ---\n"
                    context_text += f"Document: {ctx.get('doc_path', 'Unknown')}\n"
                    context_text += f"Heading: {ctx.get('heading', 'Unknown')}\n"
                    context_text += f"Content: {ctx.get('excerpt', '')}\n"
                    context_text += f"Score: {ctx.get('score', 0.0):.3f}\n"

                user_message = f"Question: {question}\n\nContext:\n{context_text}"

            # Call OpenAI API to generate the response
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using GPT-4 Turbo or similar
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            answer = response.choices[0].message.content

            # Extract sources from retrieved contexts
            sources = []
            if not selected_text and retrieved_contexts:
                for ctx in retrieved_contexts:
                    sources.append({
                        "doc_path": ctx.get("doc_path", ""),
                        "heading": ctx.get("heading", ""),
                        "excerpt": ctx.get("excerpt", "")[:200] + "..." if len(ctx.get("excerpt", "")) > 200 else ctx.get("excerpt", ""),
                        "score": ctx.get("score", 0.0)
                    })

            # Calculate response time
            latency_ms = int((__import__('time').time() - start_time) * 1000)

            return {
                "answer": answer,
                "sources": sources,
                "meta": {
                    "latency_ms": latency_ms,
                    "model": response.model,
                    "retrieval_count": len(retrieved_contexts) if retrieved_contexts else 0
                }
            }

        except Exception as e:
            logging.error(f"Error generating answer with ChatKit agent: {e}")
            latency_ms = int((__import__('time').time() - start_time) * 1000)

            return {
                "answer": "Sorry, I encountered an error while processing your question. Please try again later.",
                "sources": [],
                "meta": {
                    "latency_ms": latency_ms,
                    "model": "error",
                    "retrieval_count": 0
                }
            }

    def handle_empty_retrieval(self, question: str) -> Dict[str, Any]:
        """
        Handle the case when retrieval returns no results
        """
        start_time = __import__('time').time()

        try:
            system_message = (
                "You are an AI assistant for a textbook. "
                "The user asked a question, but no relevant content was found in the textbook. "
                "Politely inform the user that the information is not available in the current textbook content."
            )

            user_message = f"Question: {question}"

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,
                max_tokens=300
            )

            answer = response.choices[0].message.content
            latency_ms = int((__import__('time').time() - start_time) * 1000)

            return {
                "answer": answer,
                "sources": [],
                "meta": {
                    "latency_ms": latency_ms,
                    "model": response.model,
                    "retrieval_count": 0
                }
            }
        except Exception as e:
            logging.error(f"Error handling empty retrieval: {e}")
            latency_ms = int((__import__('time').time() - start_time) * 1000)

            return {
                "answer": "Sorry, I couldn't find any relevant content in the textbook to answer your question.",
                "sources": [],
                "meta": {
                    "latency_ms": latency_ms,
                    "model": "error",
                    "retrieval_count": 0
                }
            }


# Global agent instance
chatkit_agent = ChatKitAgent()