from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG-based chatbot using Cohere",
    version="1.0.0"
)

# Add CORS middleware - allow all origins for Hugging Face Spaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers that frontend can access
    expose_headers=["Access-Control-Allow-Origin"]
)

# Import and include routes
from routes import ask, ask_selected, history
import routes.streaming_ask

app.include_router(ask.router, prefix="/api", tags=["ask"])
app.include_router(ask_selected.router, prefix="/api", tags=["ask_selected"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(routes.streaming_ask.router, prefix="/api", tags=["streaming_ask"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running!"}

@app.get("/health")
async def health_check():
    # Verify all required environment variables are set
    required_vars = ["COHERE_API_KEY", "QDRANT_URL", "DATABASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        return {"status": "error", "missing_env_vars": missing_vars}

    return {"status": "healthy"}