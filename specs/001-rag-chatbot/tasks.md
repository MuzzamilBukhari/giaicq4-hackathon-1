# Implementation Tasks: RAG Chatbot Integration

## Feature Overview

Implement a Retrieval-Augmented Generation (RAG) system using FastAPI as the backend framework, Qdrant Cloud as the vector database, Neon Serverless Postgres as metadata storage, and OpenAI ChatKit Agents SDK for LLM orchestration, retrieval reasoning, and answer generation. The system will be deployed on Railway.app with an embedded Docusaurus chat widget as the frontend UI, allowing students to ask questions about textbook content and receive accurate, cited answers.

**Feature Branch**: `001-rag-chatbot`
**Created**: 2025-12-08
**Status**: Ready for Implementation

## Phase 1: Setup & Project Initialization

- [x] T001 Create backend directory structure per implementation plan
- [x] T002 Create requirements.txt with FastAPI, Qdrant, Neon, OpenAI ChatKit, Pydantic dependencies
- [x] T003 Set up Dockerfile for backend service with Python 3.11 and dependencies
- [x] T004 Create docker-compose.yml for local Qdrant and mock Neon services
- [x] T005 Create initial backend/app directory structure (main.py, config.py)

## Phase 2: Foundational Components

- [x] T006 [P] Create configuration module in backend/app/config.py with Pydantic settings
- [x] T007 [P] Set up environment variables for Qdrant, Neon, and OpenAI API keys
- [x] T008 [P] Create database connection module for Neon Postgres in backend/app/db_meta.py
- [x] T009 [P] Create Qdrant client module in backend/app/retriever.py with basic connection
- [x] T010 [P] Create basic FastAPI app structure in backend/app/main.py
- [x] T011 [P] Set up logging and request tracing for observability
- [x] T012 [P] Create health check endpoint /status in backend/app/main.py

## Phase 3: User Story 1 - Ask Questions About Textbook Content (P1)

### Story Goal
As a student or reader using the Docusaurus textbook, I want to ask questions about the book content and receive accurate, context-grounded answers so that I can better understand the material without leaving the textbook environment.

### Independent Test Criteria
Can be fully tested by asking questions about textbook content and verifying that the system returns relevant answers with proper citations to the source material.

- [x] T013 [US1] Create ChatKit agent module in backend/app/agent.py with retrieval-augmented flow
- [x] T014 [US1] Implement /query endpoint in backend/app/main.py to handle retrieval-based questions
- [x] T015 [US1] Create embedder adapter in backend/app/indexer.py for OpenAI text-embedding-3-small
- [x] T016 [US1] Implement Qdrant vector search in backend/app/retriever.py for content retrieval
- [x] T017 [US1] Create response formatting in backend/app/agent.py to include citations
- [x] T018 [US1] Implement selected text mode in /query endpoint for fallback behavior
- [x] T019 [US1] Add error handling for empty retrieval results with appropriate user messages
- [ ] T020 [US1] Create unit tests for query endpoint with mock data

## Phase 4: User Story 2 - Index Textbook Content for Search (P2)

### Story Goal
As a developer maintaining the textbook infrastructure, I want to index the textbook content so that the RAG system can retrieve relevant information when users ask questions.

### Independent Test Criteria
Can be tested by running the indexing process and verifying that content is properly chunked, embedded, and stored in the vector database with associated metadata.

- [x] T021 [US2] Create markdown parsing and heading extraction in backend/app/indexer.py
- [x] T022 [US2] Implement text chunking with 600 tokens and 80 token overlap in backend/app/indexer.py
- [x] T023 [US2] Create vector database upsert functionality in backend/app/indexer.py for Qdrant
- [x] T024 [US2] Implement metadata storage in Neon Postgres in backend/app/db_meta.py
- [x] T025 [US2] Create CLI script for indexing in scripts/index_docs.py with required flags
- [x] T026 [US2] Add validation for token count ranges (500-800) and overlap (50-120)
- [x] T027 [US2] Create indexing job tracking with status and progress in backend/app/db_meta.py
- [x] T028 [US2] Implement incremental indexing with replace/upsert options in scripts/index_docs.py
- [x] T029 [US2] Create Qdrant collection management script in scripts/qdrant_manage.py
- [ ] T030 [US2] Create unit tests for chunking and embedding functionality

## Phase 5: User Story 3 - Access RAG Chat Interface from Any Page (P3)

### Story Goal
As a textbook reader, I want to access the RAG chat interface from any page of the textbook so that I can get immediate assistance with the content I'm currently reading.

### Independent Test Criteria
Can be tested by opening the chat widget from any textbook page and verifying that it functions properly with the current page's content context.

- [x] T031 [US3] Create Docusaurus chat widget React component for frontend integration
- [x] T032 [US3] Implement selected text detection using window.getSelection() in chat widget
- [x] T033 [US3] Create API client for communicating with backend endpoints in chat widget
- [x] T034 [US3] Implement toggle for "Use selected text only" mode in chat widget
- [x] T035 [US3] Create answer display with source citations and links in chat widget
- [x] T036 [US3] Add loading and error states handling in chat widget
- [x] T037 [US3] Implement source expansion functionality in chat widget
- [x] T038 [US3] Create documentation pages under docs/rag/ for architecture and deployment
- [x] T039 [US3] Integrate chat widget into Docusaurus layout with proper styling

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T040 Implement rate limiting middleware for abuse prevention
- [x] T041 Add CORS configuration to allow only specified origins
- [x] T042 Create comprehensive API documentation with examples
- [x] T043 Add performance monitoring for query latency and success rates
- [x] T044 Implement proper error logging and monitoring
- [x] T045 Create integration tests for full query flow with sample data
- [x] T046 Set up GitHub Actions CI workflow with unit and integration tests
- [x] T047 Create Railway deployment configuration and environment setup
- [x] T048 Add documentation for troubleshooting and maintenance
- [x] T049 Perform end-to-end testing with full textbook content
- [x] T050 Deploy to Railway and validate production functionality

## Dependencies

1. **User Story 2 (Indexing)** must be completed before User Story 1 (Querying) can be fully functional, as queries require indexed content
2. User Story 3 (Frontend) depends on User Story 1 (Backend API) being available
3. Foundational components (Phase 2) must be completed before any user stories

## Parallel Execution Examples

### User Story 1 Parallel Tasks:
- T013 [P] [US1] Create ChatKit agent module
- T014 [P] [US1] Implement /query endpoint
- T015 [P] [US1] Create embedder adapter
- T016 [P] [US1] Implement Qdrant vector search

### User Story 2 Parallel Tasks:
- T021 [P] [US2] Create markdown parsing
- T022 [P] [US2] Implement text chunking
- T023 [P] [US2] Create vector database upsert
- T024 [P] [US2] Implement metadata storage

### User Story 3 Parallel Tasks:
- T031 [P] [US3] Create chat widget component
- T032 [P] [US3] Implement selected text detection
- T033 [P] [US3] Create API client

## Implementation Strategy

1. **MVP Scope**: Focus on User Story 1 (P1) with basic indexing capability (T021-T025) to enable querying
2. **Incremental Delivery**:
   - Phase 1-2: Foundation and basic query capability
   - Add User Story 2: Full indexing functionality
   - Add User Story 3: Frontend integration
   - Polish: Production readiness and deployment

3. **Testing Approach**:
   - Unit tests for individual components (T020, T030)
   - Integration tests for full query flow (T045)
   - End-to-end validation (T049)