from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

from app.config import Settings

def build_retriever(
    index: VectorStoreIndex, 
    settings: Settings, 
    topic_filter: str = None, 
    level_filter: str = None
) -> VectorIndexRetriever:
    """
    Builds a vector retriever with optional metadata filters.
    """
    filters = []
    
    if topic_filter:
        filters.append(ExactMatchFilter(key="topic", value=topic_filter))
    if level_filter:
        filters.append(ExactMatchFilter(key="level", value=level_filter))
        
    metadata_filters = MetadataFilters(filters=filters) if filters else None
    
    return VectorIndexRetriever(
        index=index,
        similarity_top_k=settings.top_k,
        filters=metadata_filters
    )
