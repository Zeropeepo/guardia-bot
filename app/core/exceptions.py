class GuardiaError(Exception):
    """Base exception class for Guardia Bot."""
    pass

class DocumentNotFoundError(GuardiaError):
    """Raised when a requested document is not found."""
    pass

class IngestionError(GuardiaError):
    """Raised when document ingestion fails."""
    pass

class RetrievalError(GuardiaError):
    """Raised when retrieval from vector store fails."""
    pass

class GuardrailViolation(GuardiaError):
    """Raised when input or output violates safety guardrails."""
    pass

class LLMError(GuardiaError):
    """Raised when communication with the LLM provider fails."""
    pass
