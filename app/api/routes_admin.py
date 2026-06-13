from fastapi import APIRouter, Depends
from app.schemas.admin import CollectionStats
from app.db.vector_store import QdrantManager, get_qdrant_manager

router = APIRouter(tags=["admin"])

@router.get("/admin/stats", response_model=CollectionStats)
def get_stats(qdrant: QdrantManager = Depends(get_qdrant_manager)):
    info = qdrant.get_collection_info()
    return CollectionStats(
        total_documents=info.get("points_count", 0),
        total_chunks=info.get("vectors_count", 0),
        collection_name=qdrant.collection_name
    )

@router.delete("/admin/collection")
def reset_collection(qdrant: QdrantManager = Depends(get_qdrant_manager)):
    qdrant.delete_collection()
    qdrant.ensure_collection()
    return {"status": "collection reset"}
