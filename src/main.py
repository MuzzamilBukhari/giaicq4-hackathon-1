from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.utils.logging import get_logger
from src.api.chat_endpoint import router as chat_router
from src.api.health_endpoint import router as health_router
from contextlib import asynccontextmanager

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events
    """
    logger.info("Starting RAG Backend Service...")

    # Startup logic can go here
    # For example: initializing connections, loading models, etc.

    yield  # This is where the application runs

    # Shutdown logic goes here
    logger.info("Shutting down RAG Backend Service...")
    # For example: closing connections, cleaning up resources, etc.


app = FastAPI(
    title="RAG Backend Service API",
    description="API for RAG chatbot functionality with Docusaurus book content",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(health_router, prefix="/api/v1", tags=["health"])

@app.get("/")
async def root():
    return {"message": "RAG Backend Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
        timeout_keep_alive=30  # Connection keep-alive timeout
    )