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
{level_instruction}

Question: {question}
Answer:"""

def build_prompt(context_chunks: list[str], question: str, level_filter: str = None) -> str:
    """Builds the final prompt combining context, the user question, and optional level instruction."""
    context_str = "\n\n".join(context_chunks)
    
    level_instruction = ""
    if level_filter:
        level_instruction = f"\nIMPORTANT: Please explain this at a {level_filter} level of understanding."
        
    return QUERY_PROMPT_TEMPLATE.format(
        context=context_str, 
        question=question,
        level_instruction=level_instruction
    )
