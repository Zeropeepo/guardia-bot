from pydantic import BaseModel
from typing import Optional

class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    topic: Optional[str] = None
    level: Optional[str] = None
    chunk_count: int
    ingested_at: str

class CollectionStats(BaseModel):
    total_documents: int
    total_chunks: int
    collection_name: str
