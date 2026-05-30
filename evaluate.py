"""
evaluate.py — standalone RAGAS evaluation script for Guardia Bot.

Usage:
    source .venv/bin/activate
    python evaluate.py

Outputs:
    - app/data/eval/results/ragas_report_<timestamp>.json
    - app/data/eval/results/ragas_report_<timestamp>.csv
"""
import json
import logging
from datetime import datetime
from pathlib import Path

from app.config import get_settings
from app.db.vector_store import get_qdrant_manager
from app.rag.ingest import IngestionService
from app.rag.pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

EVAL_FILE   = Path("app/data/eval/sample_eval.json")
RESULTS_DIR = Path("app/data/eval/results")
RAW_DIR     = Path("app/data/raw")


def ingest_all(svc: IngestionService):
    md_files = sorted(RAW_DIR.glob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No markdown files found in {RAW_DIR}")
    logger.info(f"Ingesting {len(md_files)} documents…")
    for fp in md_files:
        logger.info(f"  → {fp.name}")
        svc.ingest_file(fp, {"topic": "cybersecurity", "source": "OWASP CheatSheetSeries"})
    logger.info("Ingestion complete.")


def run_rag(pipeline: RAGPipeline, questions: list[dict]) -> dict:
    data = {"question": [], "answer": [], "contexts": [], "ground_truth": []}
    for item in questions:
        q = item["question"]
        gt = item["ground_truth"]
        logger.info(f"Querying: {q[:80]}…")
        resp = pipeline.query(q)
        data["question"].append(q)
        data["answer"].append(resp.answer)
        data["contexts"].append([s.text for s in resp.sources])
        data["ground_truth"].append(gt)
    return data


def evaluate_ragas(data: dict):
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    )
    from langchain_openai import ChatOpenAI
    from langchain_openai import OpenAIEmbeddings

    settings = get_settings()

    judge_llm = ChatOpenAI(
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.1-8b-instant",
        temperature=0.0,
    )

    dataset = Dataset.from_dict(data)
    logger.info("Running RAGAS evaluation (this may take a few minutes)…")
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=judge_llm,
        embeddings=OpenAIEmbeddings(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
            model="llama-3.1-8b-instant",
        ),
    )
    return result


def save_results(result, data: dict, questions: list[dict]):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    df = result.to_pandas()
    csv_path = RESULTS_DIR / f"ragas_report_{timestamp}.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"CSV saved → {csv_path}")

    averages = {
        col: float(df[col].mean())
        for col in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]
        if col in df.columns
    }

    report = {
        "evaluated_at": datetime.now().isoformat(),
        "num_questions": len(data["question"]),
        "model": "llama-3.1-8b-instant (Groq)",
        "embedding_model": "jina-embeddings-v3",
        "reranker": "jina-reranker",
        "documents_ingested": [p.name for p in sorted(RAW_DIR.glob("*.md"))],
        "averages": averages,
        "per_question": [
            {
                "question": row["question"],
                "ground_truth": questions[i]["ground_truth"],
                "answer": row["answer"],
                "contexts": data["contexts"][i],
                "faithfulness": float(row.get("faithfulness", 0)),
                "answer_relevancy": float(row.get("answer_relevancy", 0)),
                "context_precision": float(row.get("context_precision", 0)),
                "context_recall": float(row.get("context_recall", 0)),
            }
            for i, (_, row) in enumerate(df.iterrows())
        ],
    }

    json_path = RESULTS_DIR / f"ragas_report_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)
    logger.info(f"JSON saved → {json_path}")

    print("\n" + "="*60)
    print("  RAGAS EVALUATION RESULTS")
    print("="*60)
    for metric, score in averages.items():
        if score != score: 
            print(f"  {metric:<22} N/A (some jobs timed out)")
        else:
            bar = "█" * int(score * 20)
            print(f"  {metric:<22} {score:.4f}  |{bar:<20}|")
    print("="*60)
    print(f"\n  Full report: {json_path}\n")


def main():
    settings = get_settings()
    qdrant   = get_qdrant_manager()

    qdrant.delete_collection()
    qdrant.ensure_collection()

    ingest_svc = IngestionService(settings, qdrant)
    ingest_all(ingest_svc)

    pipeline  = RAGPipeline(settings, qdrant)
    questions = json.loads(EVAL_FILE.read_text())

    data   = run_rag(pipeline, questions)
    result = evaluate_ragas(data)
    save_results(result, data, questions)


if __name__ == "__main__":
    main()
