"""
Unit tests for complex query processing
Tests the advanced features of the RAG system
"""
import pytest
from src.nlp.query_analyzer import query_analyzer
from src.llm.prompt_engineer import prompt_engineer
from src.models.retrieved_context import RetrievedContext


def test_query_intent_analysis():
    """Test that query intent analysis works correctly"""
    # Test informational query
    info_query = "What is the capital of France?"
    analysis = query_analyzer.analyze_query_intent(info_query)
    assert analysis["query_type"] in ["informational", "explanatory"]
    assert "capital" in analysis["entities"]
    assert "france" in analysis["entities"]

    # Test procedural query
    proc_query = "How do I set up a Python virtual environment?"
    analysis = query_analyzer.analyze_query_intent(proc_query)
    assert analysis["query_type"] == "procedural"
    assert analysis["requires_multi_step_reasoning"] is True

    # Test comparative query
    comp_query = "Compare Python and JavaScript for web development"
    analysis = query_analyzer.analyze_query_intent(comp_query)
    assert analysis["query_type"] == "comparative"
    assert analysis["requires_multi_step_reasoning"] is True


def test_query_type_classification():
    """Test that query types are classified correctly"""
    # Test comparative
    assert prompt_engineer.classify_query_type("Compare A and B") == "comparative"
    assert prompt_engineer.classify_query_type("What are the differences between X and Y?") == "comparative"

    # Test procedural
    assert prompt_engineer.classify_query_type("How do I install Python?") == "procedural"
    assert prompt_engineer.classify_query_type("Steps to create a React app") == "procedural"

    # Test explanatory
    assert prompt_engineer.classify_query_type("What is machine learning?") == "explanatory"
    assert prompt_engineer.classify_query_type("Explain quantum computing") == "explanatory"

    # Test default
    assert prompt_engineer.classify_query_type("Random text") == "informational"


def test_context_relevance_scoring():
    """Test that context relevance scoring works"""
    query = "Python virtual environment setup"

    context = RetrievedContext(
        id="test-id",
        content="Python virtual environments allow you to create isolated Python environments for your projects",
        url="https://example.com",
        section="Virtual Environments",
        chunk_id="chunk-1",
        score=0.8
    )

    relevance_score = query_analyzer.get_context_relevance_score(query, context)

    # Score should be between 0 and 1
    assert 0.0 <= relevance_score <= 1.0
    # Should be relatively high since query and context share terms
    assert relevance_score > 0.3


def test_context_ranking():
    """Test that contexts are ranked by relevance correctly"""
    query = "Python virtual environment"

    contexts = [
        RetrievedContext(
            id="1",
            content="Python virtual environments allow you to create isolated Python environments for your projects",
            url="https://example.com/venv",
            section="Virtual Environments",
            chunk_id="chunk-1",
            score=0.7
        ),
        RetrievedContext(
            id="2",
            content="JavaScript frameworks like React and Vue help build user interfaces",
            url="https://example.com/js",
            section="JavaScript",
            chunk_id="chunk-2",
            score=0.5
        ),
        RetrievedContext(
            id="3",
            content="Python is a high-level programming language",
            url="https://example.com/python",
            section="Python Basics",
            chunk_id="chunk-3",
            score=0.6
        )
    ]

    ranked_contexts = query_analyzer.rank_contexts_by_relevance(query, contexts)

    # The Python virtual environment context should be ranked highest
    assert ranked_contexts[0].id == "1"
    # All contexts should be present
    assert len(ranked_contexts) == 3


def test_advanced_prompt_generation():
    """Test that advanced prompts are generated correctly"""
    query = "How do I create a Python virtual environment?"
    contexts = [
        RetrievedContext(
            id="1",
            content="Use the venv module to create virtual environments",
            url="https://example.com",
            section="Python Virtual Environments",
            chunk_id="chunk-1",
            score=0.8
        )
    ]

    advanced_prompt = prompt_engineer.create_advanced_rag_prompt(query, contexts)

    assert "system" in advanced_prompt
    assert "user" in advanced_prompt
    assert "query_type" in advanced_prompt
    assert "has_context" in advanced_prompt
    assert advanced_prompt["query_type"] == "procedural"
    assert advanced_prompt["has_context"] is True


def test_chain_of_thought_prompt():
    """Test that chain of thought prompts are generated correctly"""
    query = "Explain how neural networks work"
    contexts = [
        RetrievedContext(
            id="1",
            content="Neural networks are computing systems inspired by the human brain",
            url="https://example.com",
            section="Neural Networks",
            chunk_id="chunk-1",
            score=0.9
        )
    ]

    cot_prompt = prompt_engineer.create_contextual_chain_of_thought_prompt(query, contexts)

    assert "step by step" in cot_prompt.lower()
    assert query in cot_prompt
    assert "neural networks" in cot_prompt


if __name__ == "__main__":
    pytest.main([__file__])