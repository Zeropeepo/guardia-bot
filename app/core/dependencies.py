from fastapi import Request

def get_rag_pipeline(request: Request):
    if not hasattr(request.app.state, "rag_pipeline"):
        raise RuntimeError("RAG Pipeline not initialized")
    return request.app.state.rag_pipeline
