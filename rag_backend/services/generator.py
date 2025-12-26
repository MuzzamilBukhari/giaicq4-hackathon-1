import os
from typing import Tuple, List, Dict, Any
from .cohere_provider import CohereProvider

async def generate_answer(
    question: str,
    session_id: str,
    mode: str = "global",
    selected_text: str = None
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Generate an answer using Cohere based on the mode:
    - 'global': Uses retrieved context from Qdrant
    - 'selected': Uses only the provided selected_text
    """
    try:
        # Initialize Cohere provider
        cohere_provider = CohereProvider()

        if mode == "global":
            # Retrieve relevant chunks from Qdrant
            from .retriever import retrieve_chunks
            try:
                retrieved_chunks = await retrieve_chunks(question)

                # Build context from retrieved chunks
                context_parts = []
                citations = []

                for chunk in retrieved_chunks:
                    context_parts.append(chunk["text"])
                    citations.append(chunk["metadata"])

                context = "\n\n".join(context_parts)

                # Create prompt with context
                prompt = f"""
                You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
                Answer the user's question based ONLY on the provided context.
                If the answer cannot be found in the context, clearly state that the information is not in the textbook.

                CONTEXT:
                {context}

                QUESTION:
                {question}

                Please provide a comprehensive answer and cite the relevant sections.
                """
            except Exception as e:
                print(f"Error retrieving chunks: {e}")
                # Fallback to a general response if retrieval fails
                prompt = f"""
                You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
                I'm sorry, but I couldn't retrieve specific information from the textbook to answer your question.
                However, I can try to provide a general response based on my knowledge.

                QUESTION:
                {question}

                Please provide a helpful response to this question.
                """
                citations = []

        elif mode == "selected":
            # Use only the selected text as context
            context = selected_text
            citations = [{"text_preview": selected_text[:100] + "..." if len(selected_text) > 100 else selected_text}]

            prompt = f"""
            You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
            Answer the user's question based ONLY on the provided selected text.
            Do not use any external knowledge beyond what's in the selected text.

            SELECTED TEXT:
            {context}

            QUESTION:
            {question}

            Please provide a comprehensive answer based on this text.
            """
        else:
            raise ValueError(f"Invalid mode: {mode}")

        # Generate response using Cohere
        answer = cohere_provider.generate_text(prompt)  # Removed async call
        if not answer:
            answer = "I couldn't generate a response based on the provided context."

        return answer, citations

    except Exception as e:
        print(f"Error generating answer: {e}")
        raise


def generate_answer_streaming(
    question: str,
    session_id: str,
    mode: str = "global",
    selected_text: str = None
):
    """
    Generate an answer using Cohere with streaming support.
    """
    try:
        # Initialize Cohere provider
        cohere_provider = CohereProvider()

        if mode == "global":
            # Retrieve relevant chunks from Qdrant
            from .retriever import retrieve_chunks
            try:
                # Note: Retrieval is not streamed, but the text generation is
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                retrieved_chunks = loop.run_until_complete(retrieve_chunks(question))
                loop.close()

                # Build context from retrieved chunks
                context_parts = []
                citations = []

                for chunk in retrieved_chunks:
                    context_parts.append(chunk["text"])
                    citations.append(chunk["metadata"])

                context = "\n\n".join(context_parts)

                # Create prompt with context
                prompt = f"""
                You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
                Answer the user's question based ONLY on the provided context.
                If the answer cannot be found in the context, clearly state that the information is not in the textbook.

                CONTEXT:
                {context}

                QUESTION:
                {question}

                Please provide a comprehensive answer and cite the relevant sections.
                """
            except Exception as e:
                print(f"Error retrieving chunks: {e}")
                # Fallback to a general response if retrieval fails
                prompt = f"""
                You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
                I'm sorry, but I couldn't retrieve specific information from the textbook to answer your question.
                However, I can try to provide a general response based on my knowledge.

                QUESTION:
                {question}

                Please provide a helpful response to this question.
                """
                citations = []

        elif mode == "selected":
            # Use only the selected text as context
            context = selected_text
            citations = [{"text_preview": selected_text[:100] + "..." if len(selected_text) > 100 else selected_text}]

            prompt = f"""
            You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
            Answer the user's question based ONLY on the provided selected text.
            Do not use any external knowledge beyond what's in the selected text.

            SELECTED TEXT:
            {context}

            QUESTION:
            {question}

            Please provide a comprehensive answer based on this text.
            """
        else:
            raise ValueError(f"Invalid mode: {mode}")

        # Generate response using Cohere with streaming
        for chunk in cohere_provider.generate_text_streaming(prompt):
            yield chunk

        # Also yield the citations at the end
        yield {"citations": citations, "end": True}

    except Exception as e:
        print(f"Error generating streaming answer: {e}")
        raise