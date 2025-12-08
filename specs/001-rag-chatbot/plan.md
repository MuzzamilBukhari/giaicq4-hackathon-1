# Implementation Plan: RAG Chatbot Integration

**Branch**: `001-rag-chatbot` | **Date**: 2025-12-08 | **Spec**: [specs/001-rag-chatbot/spec.md](specs/001-rag-chatbot/spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a Retrieval-Augmented Generation (RAG) system using FastAPI as the backend framework, Qdrant Cloud as the vector database, Neon Serverless Postgres as metadata storage, and OpenAI ChatKit Agents SDK for LLM orchestration, retrieval reasoning, and answer generation. The system will be deployed on Railway.app with an embedded Docusaurus chat widget as the frontend UI, allowing students to ask questions about textbook content and receive accurate, cited answers.

## Technical Context

**Language/Version**: Python 3.11 (for backend services with FastAPI, ChatKit SDK compatibility)
**Primary Dependencies**: FastAPI, Qdrant, Neon Postgres, OpenAI ChatKit Agents SDK, Docker, Railway
**Storage**: Qdrant Cloud (vector database), Neon Serverless Postgres (metadata storage)
**Testing**: pytest (for backend unit and integration tests), GitHub Actions (for CI)
**Target Platform**: Linux server (Railway deployment), Web browser (Docusaurus frontend)
**Project Type**: Web application (backend API + frontend widget integration)
**Performance Goals**: <5s response time for queries, 99% availability during peak hours, support 50+ concurrent users
**Constraints**: Must use ChatKit Agents SDK for all LLM calls, no secrets in frontend, only /docs/ content indexed, chunk size 500-800 tokens with 50-120 overlap
**Scale/Scope**: Supports full textbook content indexing, handles student queries with proper citations, integrates seamlessly with Docusaurus

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the constitution, this feature extends the textbook with an AI assistant capability, which is outside the original constraint that stated "The constitution applies ONLY to writing the textbook content—no chatbot, authentication, personalization, or translation features at this stage." However, this addition is justified as it enhances the educational value of the textbook by providing an AI assistant that helps students understand the content, which aligns with the "Educational Clarity" principle. The implementation will maintain technical accuracy and consistency with the existing content.

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py          # FastAPI app and route mounting
│   ├── indexer.py       # docs loader, chunker, embedder_adapter, qdrant upsert
│   ├── retriever.py     # qdrant search wrapper
│   ├── agent.py         # ChatKit agent orchestration; prompt management
│   ├── db_meta.py       # Neon Postgres connector + queries
│   └── config.py        # env loader via pydantic
├── scripts/
│   ├── index_docs.py    # CLI script for indexing docs
│   └── qdrant_manage.py # helper to create/drop/list collections
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── Dockerfile
├── docker-compose.yml   # for local Qdrant + optional mock Neon
└── requirements.txt

docs/
├── rag/
│   ├── architecture.md
│   ├── deploy-railway.md
│   ├── update-index.md
│   └── troubleshooting.md

.history/prompts/rag-chatbot/  # PHR files
```

**Structure Decision**: Web application structure with separate backend (FastAPI) and frontend integration (Docusaurus plugin). The backend handles all RAG operations while the frontend provides a chat widget integrated into the existing Docusaurus documentation site.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Extension beyond original textbook scope | Enhances educational value by providing AI-assisted learning support | Manual Q&A would be less scalable and less responsive to student needs |
| Multiple technology stack (FastAPI+Qdrant+Neon+ChatKit) | Required for proper RAG implementation with vector search and metadata | Simpler approaches would not provide the accuracy and citation capabilities needed |
