# Implementation Plan: Book Website Ingestion for RAG

**Branch**: `1-book-ingestion` | **Date**: 2025-12-16 | **Spec**: [specs/1-book-ingestion/spec.md](../specs/1-book-ingestion/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Python-based ingestion pipeline that extracts text from Docusaurus book websites, chunks content deterministically, generates Cohere embeddings, and stores them in Qdrant vector database with metadata (url, section, chunk_id). The pipeline must be re-runnable without creating duplicate entries.

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv
**Storage**: Qdrant Cloud (vector database)
**Testing**: pytest
**Target Platform**: Linux server or local development environment
**Project Type**: CLI application
**Performance Goals**: Process 1000+ pages within reasonable time, handle rate limiting gracefully
**Constraints**: Must use Cohere for embeddings, Qdrant for vector storage, and only access deployed GitHub Pages URLs
**Scale/Scope**: Handle medium-sized documentation sites (up to 1000+ pages)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The implementation aligns with the project constitution:
- Technical accuracy: Using established libraries for web scraping, embeddings, and vector databases
- Educational clarity: Code will be well-documented and follow Python best practices
- Structured pedagogical flow: Pipeline follows logical sequence of fetch → extract → chunk → embed → store
- Consistency: Will follow established patterns for configuration and logging
- AI-Native workflow: Implementation supports the textbook's RAG use case

## Project Structure

### Documentation (this feature)

```text
specs/1-book-ingestion/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── book_ingestion/
│   ├── __init__.py
│   ├── fetcher.py           # Fetch book URLs and content
│   ├── extractor.py         # Extract clean text from HTML
│   ├── chunker.py           # Chunk text deterministically
│   ├── embedder.py          # Generate Cohere embeddings
│   ├── storage.py           # Qdrant vector storage operations
│   ├── logger.py            # Logging utilities
│   └── main.py              # Main ingestion pipeline entry point
├── config/
│   └── settings.py          # Configuration management
└── scripts/
    └── run_ingestion.py     # CLI entry point for the ingestion process

tests/
├── unit/
│   ├── test_fetcher.py
│   ├── test_extractor.py
│   ├── test_chunker.py
│   ├── test_embedder.py
│   └── test_storage.py
├── integration/
│   └── test_ingestion_pipeline.py
└── fixtures/
    └── sample_book_content.html

requirements.txt
requirements-dev.txt
.env.example
README.md
```

**Structure Decision**: Single CLI application project structure selected to handle the ingestion pipeline with clear separation of concerns between different components of the pipeline.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [No violations identified] | [N/A] | [N/A] |