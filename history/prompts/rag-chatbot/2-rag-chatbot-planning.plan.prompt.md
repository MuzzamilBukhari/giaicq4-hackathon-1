---
id: 2
title: rag-chatbot-planning
stage: plan
date: 2025-12-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot
branch: 001-rag-chatbot
user: Claude User
command: /sp.plan
labels: ["rag", "chatbot", "planning", "architecture", "ai"]
links:
  spec: specs/001-rag-chatbot/spec.md
  plan: specs/001-rag-chatbot/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-rag-chatbot/plan.md
 - specs/001-rag-chatbot/research.md
 - specs/001-rag-chatbot/data-model.md
 - specs/001-rag-chatbot/quickstart.md
 - specs/001-rag-chatbot/contracts/query-api.yaml
tests:
 - specs/001-rag-chatbot/plan.md validation
 - specs/001-rag-chatbot/data-model.md validation
---

## Prompt

Create:
A concrete implementation plan for the RAG Chatbot Integration that uses FastAPI + Qdrant + Neon Postgres for data, OpenAI ChatKit Agents SDK for orchestration and answer generation, and Railway.app for backend deployment. The plan must cover architecture, file placement, indexing strategy, agent orchestration design (ChatKit), CI/QA checks, Railway deployment configuration, and how the Docusaurus frontend widget integrates with the backend.

Decisions needing documentation:
- Embedding model & vector size selection (OpenAI/Claude embeddings via ChatKit) and resulting Qdrant collection vector_size.
- Chunking policy: token size (default 500–800) and overlap (50–120) and whether to use adaptive chunking for long sections.
- Qdrant collection parameters: distance metric, replicas, and payload fields (doc_path, heading, excerpt, token_count, created_at).
- Neon schema details: table design for provenance and indexing metadata and retention policy for metadata logging.
- ChatKit agent design: single retrieval-augmented agent vs. multi-agent pipeline (retriever agent + synthesize agent). Document chosen agent flow and prompt templates.
- Failure mode behavior: how the agent should respond when retrieval is empty (safe fallback), and whether to surface "no results" vs. partial answers.
- Deployment choices on Railway: Docker vs. native Railway build, autoscale settings, health checks, and environment variable handling.
- CI behavior: whether indexing is run in CI for small sample test or only in staging/prod on-demand.

Testing strategy:
- Unit tests:
  - chunking tests (ensure token counts and overlaps are correct)
  - embedder adapter tests (mock embedding provider)
  - db_meta tests (Neon insert/query)
  - retriever tests (Qdrant search returning expected ids)
- Integration tests (CI):
  - small-docs sample indexed (scripts/index_docs.py with --sample) and verify metadata rows and vector count.
  - query flow test: `POST /query` with test question returns structured JSON with `answer`, `sources[]` (path, heading, excerpt, score).
  - selected-text test: `POST /selected` returns direct answer using the provided text.
- Smoke tests (pre-deploy/local):
  - `npm run build` for Docusaurus (confirm docs/rag pages present)
  - run backend docker-compose locally (FastAPI + Qdrant local container + mock Neon) and run end-to-end query from frontend widget.
- Production validation:
  - After Railway deploy, run health endpoint `GET /status`, run sample queries, and check logs for errors and latency.
  - Validate CORS & origin restrictions (only the book domain allowed).
- Load considerations (manual):
  - Run a small burst test (10 concurrent queries) to ensure median latency is acceptable (<8s for cached retrievals) and document scaling notes for Railway.

Technical details:
- Project structure (backend):
  - backend/
    - app/main.py (FastAPI app and route mounting)
    - app/indexer.py (docs loader, chunker, embedder_adapter, qdrant upsert)
    - app/retriever.py (qdrant search wrapper)
    - app/agent.py (ChatKit agent orchestration; prompt management)
    - app/db_meta.py (Neon Postgres connector + queries)
    - app/config.py (env loader via pydantic)
    - Dockerfile
    - docker-compose.yml (for local Qdrant + optional mock Neon)
    - tests/
- ChatKit integration:
  - Use ChatKit SDK to create an agent composed of:
    1. Retriever step: call retriever.py to fetch top-k passages (with metadata)
    2. Context builder: format retrieved passages + user query into a ChatKit prompt template (include citations)
    3. ChatKit call: let ChatKit run the structured agent with `tools` disabled except retrieval helper; require structured JSON output (answer + sources list)
  - Keep agent logic modular via `agent.py` so alternative agent flows can be swapped.
- Indexing pipeline:
  - scripts/index_docs.py:
    - Walk docs/ folder, extract headings, markdown clean text, chunk by token counts, call embedder_adapter, upsert to Qdrant, insert/update metadata rows in Neon (vector_id <-> doc_path)
    - CLI flags: `--docs-path`, `--collection`, `--chunk-size`, `--overlap`, `--replace/--upsert`, `--sample`
- Qdrant:
  - Provision Qdrant Cloud collection with vector_size matching the embedding model
  - Payload: store metadata fields for provenance
  - Provide helper: scripts/qdrant_manage.py to create/drop/list collections
- Neon Postgres:
  - migrations/schema.sql with `chunks` table: id (uuid), vector_id (text), doc_path (text), heading (text), excerpt (text), token_count (int), created_at (timestamp)
  - db_meta.py to perform provenance lookups by vector_id or doc_path
- Frontend widget:
  - Docusaurus plugin or client-only React component:
    - Detect selected text via `window.getSelection()`
    - POST to backend endpoints for query/selected modes
    - Render answer with source links (use Docusaurus route structure)
    - Handle loading, errors, and source expansion
- Security:
  - All secrets stored in Railway environment variables
  - Backend checks origin/Referer header to allow requests only from the book domain(s)
  - Rate limiting basic guard (per-IP) to avoid abuse (simple in-memory limiter or middleware; document for production)
- Observability:
  - Basic request logging and structured error logs
  - Expose `/status` with: app_version, qdrant_ok, neon_ok, vector_count (sample)
- CI:
  - GitHub Actions on PRs runs unit tests + small sample index integration test (using mocked embedding provider or small sample docs)
  - On merge to main, Railway deploy is triggered automatically via Railway-GitHub integration.

Phases / milestones:
- Phase 0 — Setup & Decisions (0.5 day)
  - Configure Railway project, set env vars, provision Qdrant & Neon accounts, document choices in `specs/rag/decisions.md`.
- Phase 1 — Indexer & DB integration (1–2 days)
  - Implement chunker, embedder_adapter, Neon metadata writes, Qdrant upsert; index a small docs sample end-to-end.
- Phase 2 — Retriever & agent (1–2 days)
  - Implement retriever wrapper, design ChatKit agent flow, build prompt templates, implement `/query` and `/selected`.
- Phase 3 — Frontend widget (1 day)
  - Implement React widget and integrate into Docusaurus; connect to backend endpoints.
- Phase 4 — Tests & CI (0.5–1 day)
  - Add unit and integration tests; GitHub Actions pipeline for PRs.
- Phase 5 — Railway deployment & validation (0.5 day)
  - Build Docker image or Railway config, deploy, run validation tests, save logs to `specs/rag/build-logs.md`.
- Phase 6 — Docs & handoff (0.5 day)
  - Create `docs/rag/` pages (architecture, index instructions, deploy on Railway, troubleshooting) and finalize PR.

Deliverables:
- Backend code, Dockerfile, docker-compose for local dev
- scripts/index_docs.py and qdrant management scripts
- Neon migration SQL and db_meta helpers
- agent.py with ChatKit agent orchestration and prompt templates
- React RAG widget integrated into Docusaurus
- Tests and CI workflow
- Railway deployment with environment variables and deployment URL
- `specs/rag/` folder with decisions.md, build-logs.md, and run-verify.md

Acceptance criteria:
- Indexing a representative subset of docs completes successfully and vectors + metadata appear in Qdrant & Neon.
- `POST /query` returns structured JSON: `{ answer: string, sources: [{doc_path, heading, excerpt, score}], meta:{latency_ms, model}}`
- `POST /selected` returns an answer computed only from provided text.
- ChatKit agent used end-to-end for answer generation.
- Backend passes health checks on Railway and frontend widget can query the live endpoint.
- CI runs unit tests and the integration sample index test on PRs.

Notes & fallbacks:
- If ChatKit embedding or agent calls are rate-limited or unavailable, provide an adapter/mock that uses OpenAI raw endpoints as a temporary fallback (documented in `specs/rag/decisions.md`).
- If Railway integration is not possible, fallback to Render or Cloud Run (document why).
- Keep everything modular so embedding provider, vector DB, or agent orchestration can be swapped later.

## Response snapshot

Completed comprehensive implementation planning for RAG Chatbot Integration including:

- **Implementation Plan** (plan.md): Detailed technical context with Python 3.11, FastAPI, Qdrant, Neon Postgres, and ChatKit SDK. Project structure defined with backend/ and frontend integration in Docusaurus. Constitution check performed with justified violations for educational enhancement.

- **Research Summary** (research.md): All key decisions documented including OpenAI text-embedding-3-small model (1536-dim), 600-token chunks with 80-token overlap, cosine similarity for Qdrant, Neon schema with chunks table, single retrieval-augmented agent approach, and Railway deployment strategy.

- **Data Model** (data-model.md): Defined entities including Textbook Content Chunk, Query Request, Answer Response, and Indexing Job with validation rules, relationships, and state transitions.

- **API Contracts** (contracts/query-api.yaml): Complete OpenAPI specification for all endpoints (/query, /selected, /index, /status) with request/response schemas and error handling.

- **Quickstart Guide** (quickstart.md): Step-by-step instructions for local development, indexing, API usage, Docusaurus integration, Railway deployment, and troubleshooting.

The plan provides a complete roadmap for implementing the RAG system with FastAPI backend, Qdrant vector database, Neon metadata storage, ChatKit agent orchestration, and Railway deployment.

## Outcome

- ✅ Impact: Created complete implementation plan with architecture decisions, data models, API contracts, and deployment strategy
- 🧪 Tests: Defined comprehensive testing strategy covering unit, integration, and production validation
- 📁 Files: Generated plan.md, research.md, data-model.md, quickstart.md, and contracts/query-api.yaml
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan balances technical requirements with educational goals while maintaining system reliability

## Evaluation notes (flywheel)

- Failure modes observed: Addressed potential issues with constitution scope and complex tech stack
- Graders run and results (PASS/FAIL): PASS - all planning requirements met with detailed documentation
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with task generation to begin implementation