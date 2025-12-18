from typing import Dict, List, Optional
from src.models.retrieved_context import RetrievedContext
from src.utils.logging import get_logger
from src.llm.prompt_engineer import prompt_engineer
import re


class QueryAnalyzer:
    """
    Service for analyzing query intent and characteristics
    """
    def __init__(self):
        self.logger = get_logger(__name__)

    def analyze_query_intent(self, query: str) -> Dict[str, any]:
        """
        Analyze the intent and characteristics of a query
        """
        self.logger.info(f"Analyzing query intent: {query[:50]}...")

        # Classify query type
        query_type = prompt_engineer.classify_query_type(query)

        # Extract entities (simple keyword extraction)
        entities = self._extract_entities(query)

        # Determine complexity level
        complexity = self._determine_complexity(query)

        # Identify if query requires multi-step reasoning
        requires_reasoning = self._requires_multi_step_reasoning(query)

        analysis = {
            "query_type": query_type,
            "entities": entities,
            "complexity": complexity,
            "requires_multi_step_reasoning": requires_reasoning,
            "original_query": query
        }

        self.logger.debug(f"Query analysis result: {analysis}")
        return analysis

    def _extract_entities(self, query: str) -> List[str]:
        """
        Extract entities from the query (simplified approach)
        """
        # This is a simplified entity extraction
        # In a real implementation, you might use NER models
        words = query.lower().split()

        # Look for potential entities like technical terms, etc.
        potential_entities = []
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            # Add words that might be entities (technical terms, etc.)
            if len(clean_word) > 2:  # Skip short words
                potential_entities.append(clean_word)

        return potential_entities

    def _determine_complexity(self, query: str) -> str:
        """
        Determine the complexity level of the query
        """
        word_count = len(query.split())
        question_words = ["what", "how", "why", "when", "where", "who", "which", "whose"]

        has_question_word = any(qw in query.lower() for qw in question_words)
        has_complex_indicators = any(indicator in query.lower() for indicator in [
            "compare", "contrast", "analyze", "evaluate", "explain", "describe"
        ])

        if word_count > 20 or has_complex_indicators:
            return "high"
        elif word_count > 10 or has_question_word:
            return "medium"
        else:
            return "low"

    def _requires_multi_step_reasoning(self, query: str) -> bool:
        """
        Determine if the query requires multi-step reasoning
        """
        multi_step_indicators = [
            "compare.*and.*contrast",
            "how.*can.*i.*do.*this.*and.*that",
            "what.*is.*the.*relationship.*between",
            "analyze.*the.*pros.*and.*cons",
            "evaluate.*both.*options"
        ]

        query_lower = query.lower()
        for indicator in multi_step_indicators:
            if re.search(indicator, query_lower):
                return True

        # Check for multiple questions in one query
        question_count = query.count('?') + query_lower.count(' and ')
        return question_count > 1

    def get_context_relevance_score(
        self,
        query: str,
        context: RetrievedContext
    ) -> float:
        """
        Calculate how relevant a context is to a specific query
        """
        # Simple relevance scoring based on keyword overlap
        query_words = set(query.lower().split())
        context_words = set(context.content.lower().split())

        # Calculate intersection
        intersection = query_words.intersection(context_words)
        if not query_words:
            return 0.0

        # Return Jaccard similarity
        union = query_words.union(context_words)
        jaccard_similarity = len(intersection) / len(union) if union else 0.0

        # Also consider the original score from Qdrant
        combined_score = (jaccard_similarity + context.score) / 2

        return min(combined_score, 1.0)  # Ensure it's between 0 and 1

    def rank_contexts_by_relevance(
        self,
        query: str,
        contexts: List[RetrievedContext]
    ) -> List[RetrievedContext]:
        """
        Rank contexts by their relevance to the query
        """
        scored_contexts = []
        for context in contexts:
            relevance_score = self.get_context_relevance_score(query, context)
            # Create a new context with updated score
            updated_context = RetrievedContext(
                id=context.id,
                content=context.content,
                url=context.url,
                section=context.section,
                chunk_id=context.chunk_id,
                score=relevance_score
            )
            scored_contexts.append(updated_context)

        # Sort by score in descending order
        scored_contexts.sort(key=lambda x: x.score, reverse=True)
        return scored_contexts


# Global instance
query_analyzer = QueryAnalyzer()