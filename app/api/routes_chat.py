from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.rag.pipeline import RAGPipeline
from app.core.dependencies import get_rag_pipeline

router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
):
    print(f"[DEBUG API] Incoming Request: question='{request.question}', topic_filter='{request.topic_filter}', level_filter='{request.level_filter}'")
    return pipeline.query(
        question=request.question,
        topic_filter=request.topic_filter,
        level_filter=request.level_filter
    )
