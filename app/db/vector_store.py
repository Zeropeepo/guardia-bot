from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from llama_index.vector_stores.qdrant import QdrantVectorStore
from functools import lru_cache
import logging

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)

class QdrantManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port
        )
        self.collection_name = settings.qdrant_collection_name
        self.dimensions = settings.embedding_dimensions

    def ensure_collection(self):
        """Creates the collection if it doesn't exist."""
        if not self.client.collection_exists(self.collection_name):
            logger.info(f"Creating Qdrant collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dimensions,
                    distance=Distance.COSINE
                )
            )
        else:
            logger.info(f"Qdrant collection {self.collection_name} already exists.")

    def get_vector_store(self) -> QdrantVectorStore:
        """Returns a LlamaIndex QdrantVectorStore instance."""
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name
        )

    def get_collection_info(self) -> dict:
        """Returns statistics about the collection."""
        if self.client.collection_exists(self.collection_name):
            info = self.client.get_collection(self.collection_name)
            return {
                "status": str(info.status),
                "points_count": info.points_count,
                "vectors_count": info.points_count,
            }
        return {"status": "not_found"}

    def delete_collection(self):
        """Drops the collection."""
        if self.client.collection_exists(self.collection_name):
            logger.warning(f"Deleting Qdrant collection: {self.collection_name}")
            self.client.delete_collection(self.collection_name)

@lru_cache()
def get_qdrant_manager() -> QdrantManager:
    return QdrantManager(get_settings())
