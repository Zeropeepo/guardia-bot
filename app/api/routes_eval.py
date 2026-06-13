import json
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File

from app.schemas.eval import EvalQuestion, EvalResponse
from app.rag.evaluation import EvaluationService
from app.rag.pipeline import RAGPipeline
from app.config import get_settings
from app.core.dependencies import get_rag_pipeline

router = APIRouter(tags=["eval"])

def get_eval_service(pipeline: RAGPipeline = Depends(get_rag_pipeline)) -> EvaluationService:
    return EvaluationService(pipeline, get_settings())

@router.post("/eval", response_model=EvalResponse)
def evaluate_batch(
    questions: list[EvalQuestion],
    eval_service: EvaluationService = Depends(get_eval_service)
):
    return eval_service.evaluate(questions)

@router.post("/eval/file", response_model=EvalResponse)
def evaluate_file(
    file: UploadFile = File(...),
    eval_service: EvaluationService = Depends(get_eval_service)
):
    content = file.file.read()
    data = json.loads(content)
    questions = [EvalQuestion(**q) for q in data]
    return eval_service.evaluate(questions)
