from typing import List, Dict, Any
from src.models.retrieved_context import RetrievedContext
import re


class PromptEngineer:
    """
    Service for engineering effective prompts for the LLM
    """
    @staticmethod
    def create_rag_prompt(
        query: str,
        contexts: List[RetrievedContext],
        system_instruction: str = None
    ) -> str:
        """
        Create a RAG-appropriate prompt with context
        """
        if system_instruction is None:
            system_instruction = (
                "You are a helpful assistant that answers questions based on provided documentation. "
                "Use the following context to answer the user's question. "
                "When providing answers, please cite the relevant sources when possible."
            )

        # Format the context
        context_str = ""
        if contexts:
            context_str = "\n\nRelevant context:\n"
            for i, context in enumerate(contexts, 1):
                context_str += f"Source {i}:\n"
                context_str += f"Section: {context.section}\n"
                context_str += f"Content: {context.content}\n"
                context_str += f"URL: {context.url}\n"
                context_str += f"Relevance Score: {context.score:.2f}\n\n"

        # Create the full prompt
        full_prompt = f"{system_instruction}{context_str}\n\nQuestion: {query}\n\nAnswer:"

        return full_prompt

    @staticmethod
    def create_advanced_rag_prompt(
        query: str,
        contexts: List[RetrievedContext],
        query_type: str = "informational",
        system_instruction: str = None
    ) -> Dict[str, Any]:
        """
        Create an advanced RAG prompt with multiple components
        Returns a structured prompt with separate system, user, and context parts
        """
        if system_instruction is None:
            system_instruction = (
                "You are an expert assistant that answers questions based on provided documentation. "
                "Follow these guidelines:\n"
                "1. Answer directly and concisely based on the provided context\n"
                "2. If the context doesn't contain the answer, clearly state this\n"
                "3. Always cite the sources when providing information from the context\n"
                "4. Maintain a professional tone appropriate for technical documentation\n"
                "5. Structure your response with clear sections when appropriate"
            )

        # Classify the query type if not provided
        if not query_type:
            query_type = PromptEngineer.classify_query_type(query)

        # Format context with different strategies based on query type
        context_str = PromptEngineer._format_context_by_query_type(contexts, query_type)

        # Create different prompt variations based on query type
        user_message = f"Question: {query}\n\n"
        if context_str:
            user_message += f"Context:\n{context_str}\n\n"
        user_message += "Please provide a comprehensive answer based on the context, citing sources."

        return {
            "system": system_instruction,
            "user": user_message,
            "query_type": query_type,
            "has_context": bool(contexts)
        }

    @staticmethod
    def _format_context_by_query_type(contexts: List[RetrievedContext], query_type: str) -> str:
        """
        Format context differently based on the type of query
        """
        if not contexts:
            return ""

        if query_type == "comparative":
            # For comparative queries, highlight differences and similarities
            context_str = "Comparison Context:\n"
            for i, context in enumerate(contexts, 1):
                context_str += f"[{i}] {context.section}: {context.content}\n"
                context_str += f"Source: {context.url}\n\n"
        elif query_type == "procedural":
            # For procedural queries, focus on step-by-step information
            context_str = "Procedure Context:\n"
            for i, context in enumerate(contexts, 1):
                context_str += f"Step {i} Context - {context.section}:\n{context.content}\n"
                context_str += f"Reference: {context.url}\n\n"
        elif query_type == "explanatory":
            # For explanatory queries, focus on concepts and definitions
            context_str = "Explanatory Context:\n"
            for i, context in enumerate(contexts, 1):
                context_str += f"Concept {i} - {context.section}:\n{context.content}\n"
                context_str += f"Source: {context.url}\n\n"
        else:
            # Default formatting
            context_str = ""
            for i, context in enumerate(contexts, 1):
                context_str += f"Source {i}:\n"
                context_str += f"Section: {context.section}\n"
                context_str += f"Content: {context.content}\n"
                context_str += f"URL: {context.url}\n"
                context_str += f"Relevance Score: {context.score:.2f}\n\n"

        return context_str

    @staticmethod
    def classify_query_type(query: str) -> str:
        """
        Classify the type of query to determine the best response strategy
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())

        # Define keywords for different query types
        comparative_keywords = {"compare", "difference", "vs", "versus", "similarities", "contrast", "alternative"}
        procedural_keywords = {"how", "step", "process", "procedure", "tutorial", "guide", "implement", "create", "setup"}
        explanatory_keywords = {"what", "define", "explain", "describe", "meaning", "concept", "principle", "theory"}

        # Check for comparative keywords
        if query_words.intersection(comparative_keywords):
            return "comparative"
        # Check for procedural keywords
        elif query_words.intersection(procedural_keywords):
            return "procedural"
        # Check for explanatory keywords
        elif query_words.intersection(explanatory_keywords):
            return "explanatory"
        else:
            return "informational"

    @staticmethod
    def create_contextual_chain_of_thought_prompt(
        query: str,
        contexts: List[RetrievedContext]
    ) -> str:
        """
        Create a prompt that encourages the LLM to think step by step
        """
        system_instruction = (
            "You are an analytical assistant. For complex questions, use a step-by-step approach:\n"
            "1. Analyze the question and identify key components\n"
            "2. Review the provided context for relevant information\n"
            "3. Synthesize the information logically\n"
            "4. Provide a clear, structured answer with sources\n"
            "5. If information is insufficient, clearly state what's missing"
        )

        context_str = ""
        if contexts:
            context_str = "\n\nRelevant Context:\n"
            for i, context in enumerate(contexts, 1):
                context_str += f"[{i}] {context.section}: {context.content}\n"
                context_str += f"Source: {context.url} (Relevance: {context.score:.2f})\n\n"

        full_prompt = f"{system_instruction}{context_str}\n\nQuestion: {query}\n\nLet's think through this step by step:"
        return full_prompt

    @staticmethod
    def create_context_summary_prompt(contexts: List[RetrievedContext]) -> str:
        """
        Create a prompt to summarize the retrieved contexts
        """
        context_str = "Summarize the following contexts:\n\n"
        for i, context in enumerate(contexts, 1):
            context_str += f"{i}. {context.section}: {context.content[:200]}...\n"
            context_str += f"   Source: {context.url}\n\n"

        return context_str

    @staticmethod
    def create_qa_generation_prompt(query: str, context: str) -> str:
        """
        Create a prompt specifically for question answering with context
        """
        prompt = (
            "Based on the following context, please answer the question.\n\n"
            f"Context: {context}\n\n"
            f"Question: {query}\n\n"
            "Answer (be concise but comprehensive, and cite sources when possible):"
        )
        return prompt

    @staticmethod
    def format_sources_for_response(contexts: List[RetrievedContext]) -> List[Dict[str, Any]]:
        """
        Format contexts as sources for the response
        """
        sources = []
        for context in contexts:
            source = {
                'url': context.url,
                'section': context.section,
                'relevance_score': context.score
            }
            sources.append(source)
        return sources

    @staticmethod
    def create_fallback_prompt(query: str) -> str:
        """
        Create a fallback prompt when no relevant context is found
        """
        return (
            "You are a helpful assistant. Answer the following question to the best of your ability. "
            "If you don't know the answer, please say so clearly.\n\n"
            f"Question: {query}\n\n"
            "Answer:"
        )


# Global instance
prompt_engineer = PromptEngineer()