from pathlib import Path
from datetime import datetime, timezone
import logging
# pyrefly: ignore [missing-import]
from llama_index.core import VectorStoreIndex, Document
from llama_index.core import StorageContext

from app.config import Settings
from app.db.vector_store import QdrantManager
from app.services.embedding_service import get_embed_model
from app.services.document_service import load_documents
from app.rag.chunking import get_node_parser
from app.schemas.document import IngestResponse
from app.core.exceptions import IngestionError

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(
        self,
        settings: Settings,
        qdrant_manager: QdrantManager
    ):
        self.settings = settings
        self.qdrant_manager = qdrant_manager
        self.embed_model = get_embed_model(settings)
        self.node_parser = get_node_parser(settings)
        self.vector_store = qdrant_manager.get_vector_store()

    def _apply_metadata(self, documents: list[Document], metadata: dict):
        """Attaches metadata to documents."""
        for doc in documents:
            doc.metadata.update(metadata)
            doc.metadata["ingested_at"] = datetime.now(timezone.utc).isoformat()
            doc.excluded_embed_metadata_keys = ["ingested_at", "filename", "source"]

    def ingest_file(self, file_path: Path, additional_metadata: dict) -> IngestResponse:
        """
        Loads a single document, applies metadata, chunks it, embeds it,
        and stores it in Qdrant.
        """
        try:
            logger.info(f"Starting ingestion for file: {file_path}")
            documents = load_documents(file_path)
            
            if not documents:
                raise IngestionError("No text found in document.")
                
            base_metadata = {
                "filename": file_path.name,
                "source": str(file_path)
            }
            base_metadata.update(additional_metadata)
            
            self._apply_metadata(documents, base_metadata)

            nodes = self.node_parser.get_nodes_from_documents(documents)
            storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

            VectorStoreIndex(
                nodes,
                storage_context=storage_context,
                embed_model=self.embed_model,
                show_progress=True
            )
            
            logger.info(f"Successfully ingested {file_path.name} into {len(nodes)} chunks.")
            
            return IngestResponse(
                document_id=documents[0].doc_id,
                filename=file_path.name,
                num_chunks=len(nodes),
                status="success"
            )
            
        except Exception as e:
            logger.error(f"Failed to ingest {file_path}: {str(e)}")
            raise IngestionError(f"Ingestion failed: {str(e)}") from e
