from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    question: str
    topic_filter: Optional[str] = None
    level_filter: Optional[str] = None

class SourceChunk(BaseModel):
    text: str
    document_title: str
    page_or_section: Optional[str] = None
    relevance_score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    latency_ms: float
