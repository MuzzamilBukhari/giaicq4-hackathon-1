---
id: 1
title: rag-chatbot-specification
stage: spec
date: 2025-12-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot
branch: 001-rag-chatbot
user: Claude User
command: /sp.specify
labels: ["rag", "chatbot", "specification", "ai"]
links:
  spec: specs/001-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-rag-chatbot/spec.md
 - specs/001-rag-chatbot/checklists/requirements.md
tests:
 - specs/001-rag-chatbot/spec.md validation
---

## Prompt

RAG Chatbot Integration using FastAPI, Qdrant, Neon Postgres, and OpenAI ChatKit Agents SDK — Deploy on Railway

Target audience:
Students and readers using the Docusaurus textbook who need an accurate AI assistant that can answer questions grounded strictly in the book content. Developers maintaining the backend and infrastructure.

Focus:
Implement a Retrieval-Augmented Generation (RAG) system using:
- **FastAPI** as the backend framework
- **Qdrant Cloud** as the vector database
- **Neon Serverless Postgres** as metadata storage
- **OpenAI ChatKit Agents SDK** for LLM orchestration, retrieval reasoning, and answer generation
- **Railway.app** as the deployment platform for hosting the backend (always-on, secure environment)
- **Embedded Docusaurus Chat Widget** as the frontend UI

Success criteria:
- Fully working RAG backend deployed on **Railway**, with secure environment variables and a stable API endpoint.
- Backend exposes endpoints:
  - `POST /index` — chunk markdown files under `/docs/`, embed using ChatKit embedding tools, store vectors in Qdrant, metadata in Neon Postgres.
  - `POST /query` — run retrieval + LLM reasoning using ChatKit Agents; return answer + citations.
  - `POST /selected` — answer based strictly on highlighted text (no vector lookup).
  - `GET /status` — health check endpoint.
- Retrieval powered by **Qdrant** with:
  - Proper collection schema
  - Metadata mapping: doc_path, heading, chunk_text, token_count, created_at
- ChatKit Agents SDK powers:
  - Retrieval-augmented answer generation
  - Source grounding
  - Structured output for citations
  - Configurable agent reasoning style
- Frontend RAG widget integrated into Docusaurus:
  - Opens as a modal/panel from any page
  - Detects highlighted text
  - Toggle: "Use selected text only"
  - Displays answer + sources + links to doc headings
  - Uses only the backend endpoint (no API keys leaked)
- Deployment on **Railway**:
  - Dockerfile or Railway Nix build
  - Environment variables set in Railway dashboard
  - Automatic deploy on `main` updates
  - Railway logs + metrics enabled
- Documentation pages added under `docs/rag/`:
  - Architecture overview
  - Indexing instructions
  - How to deploy on Railway
  - Troubleshooting

Constraints:
- All LLM calls must be routed through **ChatKit Agents SDK** — no raw completion calls in this iteration.
- Do not store or expose any secrets in frontend code.
- Only textbook content in `/docs/` may be indexed (no external web crawling).
- Chunk size default: 500–800 tokens; overlap: 50–120 tokens.
- Selected-text queries must bypass retrieval entirely and rely solely on provided context.

Deliverables:
1. **Backend (FastAPI)**
   - `main.py` with endpoints
   - `indexer.py` (chunk → embed → store)
   - `retriever.py` (Qdrant search)
   - `agent.py` using ChatKit Agents SDK for orchestration and answer generation
   - `db_meta.py` for Neon queries
   - Dockerfile + Railway deployment config
   - Unit tests for indexing, retrieval, and answer formatting

2. **Indexing Pipeline**
   - CLI tool: `scripts/index_docs.py`
   - Upsert mode for incremental updates
   - Logging and error handling

3. **Databases**
   - Qdrant: create collection automatically with vector size from chosen embedding model
   - Neon: table schema creation SQL + migration notes

4. **Frontend RAG Widget**
   - React component (Docusaurus plugin)
   - API integration
   - Answer viewer with citation box
   - Selected-text extraction logic

5. **Documentation**
   - `/docs/rag/architecture.md`
   - `/docs/rag/deploy-railway.md`
   - `/docs/rag/update-index.md`
   - `/docs/rag/troubleshooting.md`

6. **Deployment**
   - Backend deployed on Railway with persistent environment variables
   - Production URL provided
   - Build logs saved in `specs/rag/build-logs.md`

Success checkpoints:
- Qdrant & Neon connections tested using Railway environment variables
- Full index of `/docs/` completed without errors
- Query returns answer + citations in structured JSON from ChatKit agent
- Frontend widget can query backend

## Response snapshot

Created comprehensive feature specification for RAG Chatbot Integration including:
- User stories with priorities (P1-P3) covering core functionality
- Functional requirements (FR-001 to FR-013) detailing system capabilities
- Key entities definition for data structures
- Success criteria with measurable outcomes (SC-001 to SC-007)
- Edge cases identification
- Quality validation checklist confirming all requirements met

Specification covers the core functionality: allowing students to ask questions about textbook content and receive accurate, cited answers via a chat interface integrated into the Docusaurus textbook. Includes indexing of textbook content, vector search capabilities, and deployment on Railway.

## Outcome

- ✅ Impact: Created complete feature specification for RAG chatbot system with 13 functional requirements, 3 user stories, and 7 success criteria
- 🧪 Tests: Specification validated against quality checklist with all items passing
- 📁 Files: Created spec.md and requirements.md checklist in specs/001-rag-chatbot/
- 🔁 Next prompts: Ready for /sp.clarify or /sp.plan to proceed with feature development
- 🧠 Reflection: Specification successfully abstracts implementation details while focusing on user value and measurable outcomes

## Evaluation notes (flywheel)

- Failure modes observed: None - specification meets all quality criteria
- Graders run and results (PASS/FAIL): PASS - all validation items completed successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with planning phase to design technical architecture