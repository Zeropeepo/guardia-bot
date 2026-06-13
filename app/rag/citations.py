from llama_index.core.schema import NodeWithScore
from app.schemas.chat import SourceChunk

def format_sources(nodes: list[NodeWithScore]) -> list[SourceChunk]:
    """
    Extracts source metadata and relevance scores from retrieved nodes.
    """
    sources = []
    
    for node in nodes:
        text = node.node.get_content().strip()
        filename = node.node.metadata.get("filename", "Unknown Document")
        score = float(node.score) if node.score is not None else 0.0
        
        sources.append(SourceChunk(
            text=text,
            document_title=filename,
            page_or_section=node.node.metadata.get("page_label"),
            relevance_score=score
        ))
        
    return sources
