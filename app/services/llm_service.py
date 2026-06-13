from llama_index.llms.openai_like import OpenAILike
from app.config import Settings

def get_llm(settings: Settings) -> OpenAILike:
    """
    Returns a configured OpenAILike instance pointing to the Groq API.
    Uses temperature 0.3, which is appropriate for educational use cases.
    """
    return OpenAILike(
        api_key=settings.groq_api_key,
        api_base="https://api.groq.com/openai/v1",
        model=settings.groq_model_name,
        is_chat_model=True,
        temperature=0.3,
        max_tokens=1024
    )
