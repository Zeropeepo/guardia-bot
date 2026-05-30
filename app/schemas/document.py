from pydantic import BaseModel
from typing import Optional

class IngestRequest(BaseModel):
    topic: Optional[str] = None
    level: Optional[str] = None

class IngestResponse(BaseModel):
    document_id: str
    filename: str
    num_chunks: int
    status: str
