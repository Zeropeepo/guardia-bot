from llama_index.core.node_parser import SentenceSplitter
from app.config import Settings

def get_node_parser(settings: Settings) -> SentenceSplitter:
    """Returns a configured SentenceSplitter for document chunking."""
    return SentenceSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )
