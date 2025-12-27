"""
pi-rag - Local RAG system using llama-cpp-python

Components:
- ModelManager: Multi-model load/unload management
- EmbeddingService: Generate embeddings using GGUF models
- VectorStore: CPU-based vector storage with cosine similarity
- Retriever: Semantic document search
- RAGOrchestrator: Coordinate retrieval and LLM generation
- ingest_file/ingest_directory: Document ingestion tools
"""

from .model_manager import ModelManager, ModelConfig, get_model_manager
from .vectorstore import VectorStore
from .embedding import EmbeddingService, get_embedding_service
from .retriever import Retriever, get_retriever
from .orchestrator import RAGOrchestrator, get_orchestrator
from .ingest import ingest_file, ingest_text, chunk_text
from .bulk_ingest import ingest_directory

__all__ = [
    # Model Management
    'ModelManager',
    'ModelConfig', 
    'get_model_manager',
    
    # Vector Store
    'VectorStore',
    
    # Embeddings
    'EmbeddingService',
    'get_embedding_service',
    
    # Retrieval
    'Retriever',
    'get_retriever',
    
    # Orchestration
    'RAGOrchestrator',
    'get_orchestrator',
    
    # Ingestion
    'ingest_file',
    'ingest_text',
    'ingest_directory',
    'chunk_text',
]

__version__ = "1.0.0"
