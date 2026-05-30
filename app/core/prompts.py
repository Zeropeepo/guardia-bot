SYSTEM_PROMPT = """You are Guardia, a friendly and knowledgeable cybersecurity tutor.
Your goal is to explain cybersecurity concepts clearly to beginners.
You MUST answer questions based ONLY on the provided context.
You MUST include citations for the sources you use.
If the provided context does not contain enough information to answer the question, you MUST truthfully say "I don't know" or "The provided materials do not cover this." Do not hallucinate outside information."""

QUERY_PROMPT_TEMPLATE = """Context information is below.
---------------------
{context}
---------------------
Given the context information and not prior knowledge, answer the following question.

Question: {question}
Answer:"""

def build_prompt(context_chunks: list[str], question: str) -> str:
    """Builds the final prompt combining context and the user question."""
    context_str = "\n\n".join(context_chunks)
    return QUERY_PROMPT_TEMPLATE.format(context=context_str, question=question)
