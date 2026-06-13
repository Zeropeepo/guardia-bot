from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Keys & LLM settings
    jina_api_key: str = ""
    mimo_api_key: str = ""
    mimo_base_url: str = "https://api.mimo.ai/v1"
    mimo_model_name: str = "mimo-text-model"
    groq_api_key: str = ""
    groq_model_name: str = "llama-3.3-70b-versatile"

    # Qdrant Vector Store
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "guardia_docs"

    # RAG Settings
    embedding_model_name: str = "jina-embeddings-v3"
    embedding_dimensions: int = 1024
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 10
    rerank_top_k: int = 3

    # Application Settings
    log_level: str = "INFO"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    """
    return Settings()
