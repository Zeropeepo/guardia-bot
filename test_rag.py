import sys
import asyncio
from pathlib import Path
from app.config import get_settings
from app.db.vector_store import get_qdrant_manager
from app.rag.ingest import IngestionService
from app.rag.pipeline import RAGPipeline

def test():
    settings = get_settings()
    qdrant = get_qdrant_manager()
    qdrant.delete_collection()
    qdrant.ensure_collection()
    
    # 1. Ingest
    ingest_svc = IngestionService(settings, qdrant)
    
    docs_dir = Path("app/data/raw")
    md_files = list(docs_dir.glob("*.md"))
    
    if not md_files:
        print("No markdown files found in app/data/raw/")
        return
        
    for file_path in md_files:
        print(f"Ingesting {file_path.name}...")
        ingest_svc.ingest_file(file_path, {"topic": "cybersecurity"})
        
    # 2. Query
    pipeline = RAGPipeline(settings, qdrant)
    
    questions = [
        "What is SQL Injection and how can I prevent it?",
        "What are the best practices for preventing Cross-Site Scripting (XSS)?"
    ]
    
    for q in questions:
        print(f"\n======================================")
        print(f"Querying: {q}")
        print(f"======================================\n")
        resp = pipeline.query(q)
        
        print("\n--- Answer ---")
        print(resp.answer)
        print("\n--- Sources ---")
        for src in resp.sources:
            print(f"- {src.document_title} (Score: {src.relevance_score:.2f})")

if __name__ == "__main__":
    test()
