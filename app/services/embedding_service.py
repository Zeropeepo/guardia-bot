from llama_index.embeddings.jinaai import JinaEmbedding
from app.config import Settings

def get_embed_model(settings: Settings) -> JinaEmbedding:
    """Returns a configured JinaEmbedding instance."""
    return JinaEmbedding(
        api_key=settings.jina_api_key,
        model=settings.embedding_model_name,
        embed_batch_size=16
    )
