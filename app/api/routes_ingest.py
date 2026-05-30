from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from pathlib import Path

from app.schemas.document import IngestResponse
from app.rag.ingest import IngestionService
from app.config import get_settings, Settings
from app.db.vector_store import get_qdrant_manager
from app.services.document_service import load_uploaded_file

router = APIRouter(tags=["ingest"])

def get_ingestion_service() -> IngestionService:
    settings = get_settings()
    qdrant = get_qdrant_manager()
    return IngestionService(settings, qdrant)

@router.post("/ingest", response_model=IngestResponse)
def ingest_document(
    file: UploadFile = File(...),
    topic: Optional[str] = Form(None),
    level: Optional[str] = Form(None),
    service: IngestionService = Depends(get_ingestion_service)
):
    save_dir = Path("app/data/raw")
    file_path = load_uploaded_file(file, save_dir)
    
    metadata = {}
    if topic:
        metadata["topic"] = topic
    if level:
        metadata["level"] = level
        
    response = service.ingest_file(file_path, metadata)
    return response
