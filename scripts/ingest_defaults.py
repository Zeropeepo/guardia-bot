import asyncio
import sys
import os
from pathlib import Path

# Add the root directory to PYTHONPATH so it can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings
from app.db.vector_store import get_qdrant_manager
from app.rag.ingest import IngestionService

def main():
    print("Starting default ingestion process...")
    settings = get_settings()
    qdrant = get_qdrant_manager()
    service = IngestionService(settings, qdrant)
    
    info = qdrant.get_collection_info()
    if info.get("points_count", 0) > 0:
        print(f"Collection already populated with {info['points_count']} chunks. Skipping ingestion.")
        return
        
    raw_dir = Path("app/data/raw")
    if not raw_dir.exists():
        print(f"Error: Directory {raw_dir} does not exist.")
        return

    md_files = list(raw_dir.glob("*.md"))
    if not md_files:
        print("No markdown files found to ingest.")
        return

    print(f"Found {len(md_files)} files. Ingesting...")
    
    success_count = 0
    for file_path in md_files:
        print(f" -> Ingesting {file_path.name}...")
        try:
            service.ingest_file(file_path, {"topic": "cybersecurity_cheatsheet"})
            success_count += 1
        except Exception as e:
            print(f"    [Error] Failed to ingest {file_path.name}: {e}")

    print(f"Ingestion complete! Successfully ingested {success_count}/{len(md_files)} files.")

if __name__ == "__main__":
    main()
