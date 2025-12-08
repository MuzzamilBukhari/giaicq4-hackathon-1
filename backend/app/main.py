from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings
from .db_meta import db_manager
from .retriever import qdrant_manager
from .agent import chatkit_agent
from .rate_limiter import rate_limiter
from .metrics import perf_monitor
from .logging_config import setup_logging
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
import time
import asyncio

# Setup logging
setup_logging()

# Initialize settings
settings = Settings()

# Create FastAPI app instance
app = FastAPI(
    title="RAG Chatbot API",
    description="API for querying textbook content with retrieval-augmented generation",
    version="1.0.0"
)

# Add CORS middleware
allowed_origins = [origin.strip() for origin in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class QueryRequest(BaseModel):
    question: str
    mode: str = "full_retrieval"  # 'full_retrieval' or 'selected_text_only'
    selected_text: Optional[str] = None


class SelectedTextRequest(BaseModel):
    question: str
    selected_text: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list
    meta: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running"}

@app.post("/query", response_model=AnswerResponse)
async def query_endpoint(request: QueryRequest, req: Request) -> AnswerResponse:
    """
    Query textbook content with retrieval-augmented generation
    """
    start_time = time.time()

    # Get client IP for rate limiting
    client_ip = req.client.host
    if not rate_limiter.is_allowed(client_ip):
        # Record this as an error for metrics
        latency_ms = (time.time() - start_time) * 1000
        perf_monitor.record_request(latency_ms, success=False)
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

    try:
        if request.mode == "selected_text_only":
            if not request.selected_text:
                # Record this as an error for metrics
                latency_ms = (time.time() - start_time) * 1000
                perf_monitor.record_request(latency_ms, success=False)
                raise HTTPException(status_code=400, detail="selected_text is required for selected_text_only mode")

            # Generate answer using only the selected text
            result = chatkit_agent.generate_answer_with_citations(
                question=request.question,
                retrieved_contexts=[],
                selected_text=request.selected_text
            )
        else:  # full_retrieval mode
            # First, connect to Qdrant if not already connected
            await qdrant_manager.connect()

            # Generate embedding for the question
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
            embedding_response = client.embeddings.create(
                input=request.question,
                model="text-embedding-3-small"  # Using the same model as specified in research
            )
            query_vector = embedding_response.data[0].embedding

            # Search for similar content in Qdrant
            search_results = await qdrant_manager.search_vectors(query_vector, limit=5)

            if not search_results:
                # Handle empty retrieval case
                result = chatkit_agent.handle_empty_retrieval(request.question)
            else:
                # Format search results for the agent
                formatted_contexts = []
                vector_ids = []

                for result in search_results:
                    payload = result["payload"]
                    formatted_contexts.append({
                        "doc_path": payload.get("doc_path", ""),
                        "heading": payload.get("heading", ""),
                        "excerpt": payload.get("excerpt", ""),
                        "score": result["score"]
                    })
                    vector_ids.append(result["id"])

                # Get additional metadata from Neon if needed
                if vector_ids:
                    chunks = await db_manager.get_chunks_by_vector_ids(vector_ids)
                    # We already have the metadata from Qdrant payload, so we can use formatted_contexts as is

                # Generate answer with citations
                result = chatkit_agent.generate_answer_with_citations(
                    question=request.question,
                    retrieved_contexts=formatted_contexts
                )

        # Calculate and record latency
        latency_ms = (time.time() - start_time) * 1000
        perf_monitor.record_request(latency_ms, success=True)

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            meta=result["meta"]
        )
    except Exception as e:
        # Record error for metrics
        latency_ms = (time.time() - start_time) * 1000
        perf_monitor.record_request(latency_ms, success=False)
        logging.error(f"Error in query endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/selected", response_model=AnswerResponse)
async def selected_text_endpoint(request: SelectedTextRequest, req: Request) -> AnswerResponse:
    """
    Query using selected text only (no vector lookup)
    """
    start_time = time.time()

    # Get client IP for rate limiting
    client_ip = req.client.host
    if not rate_limiter.is_allowed(client_ip):
        # Record this as an error for metrics
        latency_ms = (time.time() - start_time) * 1000
        perf_monitor.record_request(latency_ms, success=False)
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

    try:
        result = chatkit_agent.generate_answer_with_citations(
            question=request.question,
            retrieved_contexts=[],
            selected_text=request.selected_text
        )

        # Calculate and record latency
        latency_ms = (time.time() - start_time) * 1000
        perf_monitor.record_request(latency_ms, success=True)

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            meta=result["meta"]
        )
    except Exception as e:
        # Record error for metrics
        latency_ms = (time.time() - start_time) * 1000
        perf_monitor.record_request(latency_ms, success=False)
        logging.error(f"Error in selected text endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing selected text query: {str(e)}")


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Performance metrics endpoint
    """
    return perf_monitor.get_metrics()


@app.get("/status")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint that verifies the status of all dependencies
    """
    status = "healthy"
    qdrant_ok = False
    neon_ok = False
    vector_count = 0

    try:
        # Check Qdrant connection
        await qdrant_manager.connect()
        await qdrant_manager.ensure_collection_exists()
        vector_count = await qdrant_manager.get_vector_count()
        qdrant_ok = True
    except Exception as e:
        logging.error(f"Qdrant health check failed: {e}")
        status = "degraded"

    try:
        # Check Neon connection
        await db_manager.connect()
        await db_manager.create_tables()
        neon_ok = True
    except Exception as e:
        logging.error(f"Neon health check failed: {e}")
        status = "degraded"

    # Include performance metrics in the status response
    perf_metrics = perf_monitor.get_metrics()

    return {
        "status": status,
        "app_version": "1.0.0",
        "qdrant_ok": qdrant_ok,
        "neon_ok": neon_ok,
        "vector_count": vector_count,
        "performance_metrics": perf_metrics
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)