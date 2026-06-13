from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

from app.config import Settings

def build_retriever(
    index: VectorStoreIndex, 
    settings: Settings
) -> VectorIndexRetriever:
    """
    Builds a vector retriever for fetching relevant context.
    """
    return VectorIndexRetriever(
        index=index,
        similarity_top_k=settings.top_k
    )
