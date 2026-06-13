from pydantic import BaseModel
from typing import Optional, List, Dict

class EvalQuestion(BaseModel):
    question: str
    ground_truth: str
    expected_topic: Optional[str] = None

class EvalResult(BaseModel):
    question: str
    answer: str
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float

class EvalResponse(BaseModel):
    results: List[EvalResult]
    averages: Dict[str, float]
