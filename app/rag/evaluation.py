import logging
from langchain_groq import ChatGroq
from app.config import Settings
from app.schemas.eval import EvalQuestion, EvalResult, EvalResponse
from app.rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)

class EvaluationService:
    def __init__(self, pipeline: RAGPipeline, settings: Settings):
        self.pipeline = pipeline
        self.settings = settings
        
        self.judge_llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.groq_model_name,
            temperature=0.0
        )

    def evaluate(self, questions: list[EvalQuestion]) -> EvalResponse:
        try:
            from datasets import Dataset
            from ragas import evaluate
            from ragas.metrics import (
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            )
        except ImportError as e:
            raise RuntimeError(f"ragas or datasets not installed: {e}")

        data = {
            "question": [],
            "answer": [],
            "contexts": [],
            "ground_truth": []
        }
        
        results = []
        
        for q in questions:
            resp = self.pipeline.query(
                question=q.question,
                topic_filter=q.expected_topic
            )
            contexts = [src.text for src in resp.sources]
            
            data["question"].append(q.question)
            data["answer"].append(resp.answer)
            data["contexts"].append(contexts)
            data["ground_truth"].append(q.ground_truth)
            
        dataset = Dataset.from_dict(data)
        
        logger.info("Running RAGAS evaluation...")
        evaluation_result = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ],
            llm=self.judge_llm
        )
        
        scores_df = evaluation_result.to_pandas()
        
        for idx, row in scores_df.iterrows():
            results.append(EvalResult(
                question=row['question'],
                answer=row['answer'],
                faithfulness=row.get('faithfulness', 0.0),
                answer_relevancy=row.get('answer_relevancy', 0.0),
                context_precision=row.get('context_precision', 0.0),
                context_recall=row.get('context_recall', 0.0)
            ))
            
        averages = {
            "faithfulness": scores_df['faithfulness'].mean() if 'faithfulness' in scores_df else 0.0,
            "answer_relevancy": scores_df['answer_relevancy'].mean() if 'answer_relevancy' in scores_df else 0.0,
            "context_precision": scores_df['context_precision'].mean() if 'context_precision' in scores_df else 0.0,
            "context_recall": scores_df['context_recall'].mean() if 'context_recall' in scores_df else 0.0,
        }
        
        return EvalResponse(results=results, averages=averages)
