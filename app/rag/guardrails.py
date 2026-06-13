from app.core.security import sanitize_input, detect_injection
from app.core.exceptions import GuardrailViolation
import logging

logger = logging.getLogger(__name__)

def validate_input(question: str) -> str:
    """
    Validates user input against injection attacks and sanitizes it.
    """
    clean_question = sanitize_input(question)
    
    if not clean_question:
        raise GuardrailViolation("Question cannot be empty after sanitization.")
        
    if detect_injection(clean_question):
        logger.warning(f"Injection attempt detected in input: {question}")
        raise GuardrailViolation("Input rejected due to potential prompt injection attempt.")
        
    return clean_question

def validate_output(response: str) -> str:
    """
    Validates LLM output. In v1, this is a simple passthrough.
    """
    if not response:
        raise GuardrailViolation("LLM generated an empty response.")
        
    return response
