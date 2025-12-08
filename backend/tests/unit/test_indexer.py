"""
Unit tests for the indexer module
"""
import pytest
from app.indexer import EmbedderAdapter


def test_count_tokens():
    """Test token counting functionality"""
    adapter = EmbedderAdapter()
    text = "This is a test sentence."
    token_count = adapter.count_tokens(text)

    # The exact count may vary based on the tokenizer, but it should be reasonable
    assert isinstance(token_count, int)
    assert token_count > 0


def test_chunk_text():
    """Test text chunking functionality"""
    adapter = EmbedderAdapter()
    text = "This is a test sentence. " * 50  # Create a longer text
    chunks = adapter.chunk_text(text, chunk_size=30, overlap=5)

    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert all(len(chunk) > 0 for chunk in chunks)


def test_extract_headings():
    """Test heading extraction from markdown"""
    adapter = EmbedderAdapter()
    markdown_text = """# Introduction
This is the introduction.

## Background
Some background information.

### Details
More details here.
"""

    headings_content = adapter.extract_headings(markdown_text)

    assert len(headings_content) > 0
    assert isinstance(headings_content[0], tuple)
    assert len(headings_content[0]) == 2  # (heading, content)