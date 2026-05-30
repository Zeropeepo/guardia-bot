import logging
from llama_index.core.llms import LLM, ChatMessage, MessageRole
from app.core.prompts import build_prompt, SYSTEM_PROMPT
from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)

def generate_response(llm: LLM, context_chunks: list[str], question: str) -> str:
    """
    Assembles the prompt and calls the LLM to generate a response.
    """
    prompt = build_prompt(context_chunks, question)
    
    try:
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=SYSTEM_PROMPT),
            ChatMessage(role=MessageRole.USER, content=prompt)
        ]
        
        response = llm.chat(messages)
        return response.message.content
        
    except Exception as e:
        logger.error(f"LLM Generation failed: {str(e)}")
        raise LLMError(f"Failed to generate response: {str(e)}") from e
