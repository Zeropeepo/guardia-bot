import time
import logging
# pyrefly: ignore [missing-import]
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings as LlamaSettings
from llama_index.core.schema import QueryBundle

from app.config import Settings
from app.db.vector_store import QdrantManager
from app.services.embedding_service import get_embed_model
from app.services.llm_service import get_llm
from app.rag.retrieval import build_retriever
from app.rag.reranking import get_reranker
from app.rag.generation import generate_response
from app.rag.citations import format_sources
from app.rag.guardrails import validate_input, validate_output
from app.schemas.chat import ChatResponse
from app.core.exceptions import RetrievalError

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, settings: Settings, qdrant_manager: QdrantManager):
        self.settings = settings
        self.qdrant_manager = qdrant_manager
        
        self.embed_model = get_embed_model(settings)
        self.llm = get_llm(settings)
        self.reranker = get_reranker(settings)
        self.vector_store = qdrant_manager.get_vector_store()
        
        LlamaSettings.embed_model = self.embed_model
        LlamaSettings.llm = self.llm
        
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            embed_model=self.embed_model
        )

    def query(self, question: str, topic_filter: str = None, level_filter: str = None) -> ChatResponse:
        """
        Executes the full RAG pipeline: retrieval -> reranking -> generation.
        """
        start_time = time.time()
        
        # 1. Guardrails & Validation
        safe_question = validate_input(question)
        logger.info(f"Processing query: {safe_question}")
        
        try:
            retrieval_query = f"[Context Topic: {topic_filter}] {safe_question}" if topic_filter else safe_question
            
            # 2. Retrieval
            retriever = build_retriever(
                index=self.index, 
                settings=self.settings
            )
            retrieved_nodes = retriever.retrieve(retrieval_query)
            logger.info(f"Retrieved {len(retrieved_nodes)} initial nodes.")
            
            # 3. Reranking
            if retrieved_nodes:
                query_bundle = QueryBundle(query_str=retrieval_query)
                reranked_nodes = self.reranker.postprocess_nodes(
                    retrieved_nodes, query_bundle=query_bundle
                )
                logger.info(f"Reranked down to {len(reranked_nodes)} nodes.")
            else:
                reranked_nodes = []
                
            # 4. Context Assembly
            context_chunks = [node.node.get_content() for node in reranked_nodes]
            
            # 5. Generation
            raw_response = generate_response(self.llm, context_chunks, safe_question, level_filter)
            
            # 6. Output Guardrails
            safe_response = validate_output(raw_response)
            
            # 7. Citations
            sources = format_sources(reranked_nodes)
            
            latency_ms = (time.time() - start_time) * 1000
            
            return ChatResponse(
                answer=safe_response,
                sources=sources,
                latency_ms=latency_ms
            )
            
        except Exception as e:
            logger.error(f"RAG Pipeline failed: {str(e)}")
            raise RetrievalError(f"Failed to process query: {str(e)}") from e
