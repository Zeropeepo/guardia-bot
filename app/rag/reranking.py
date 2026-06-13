from llama_index.postprocessor.jinaai_rerank import JinaRerank
from app.config import Settings

def get_reranker(settings: Settings) -> JinaRerank:
    """Returns a configured JinaRerank instance."""
    return JinaRerank(
        api_key=settings.jina_api_key,
        top_n=settings.rerank_top_k
    )
