from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.core.logging import setup_logging
from app.core.exceptions import GuardiaError
from app.db.vector_store import get_qdrant_manager
from app.rag.pipeline import RAGPipeline
from app.api import routes_chat, routes_ingest, routes_admin, routes_eval

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    settings = get_settings()
    setup_logging(settings.log_level)
    logger.info("Starting Guardia Bot...")
    
    try:
        qdrant_manager = get_qdrant_manager()
        qdrant_manager.ensure_collection()
        
        app.state.rag_pipeline = RAGPipeline(settings, qdrant_manager)
        logger.info("RAG Pipeline initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize core components: {e}")
        raise
    
    yield
    logger.info("Shutting down Guardia Bot...")

app = FastAPI(
    title="Guardia Bot API",
    description="Cybersecurity Educational RAG Chatbot",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(GuardiaError)
async def guardia_error_handler(request: Request, exc: GuardiaError):
    logger.error(f"Guardia error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

app.include_router(routes_chat.router, prefix="/api")
app.include_router(routes_ingest.router, prefix="/api")
app.include_router(routes_admin.router, prefix="/api")
app.include_router(routes_eval.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
