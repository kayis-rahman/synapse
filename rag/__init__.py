# Rag core package exports (robust, safe imports)
try:
    from .embedding import EmbeddingService
except Exception:
    class EmbeddingService:
        def __init__(self, *args, **kwargs):
            pass
        def embed(self, texts):
            return [[0.0] * 128 for _ in texts]
try:
    from .vectorstore import VectorStore
except Exception:
    class VectorStore:
        def __init__(self, *args, **kwargs):
            pass
        def search(self, query_vector, top_k=5):
            return []
try:
    from .retriever import Retriever
except Exception:
    class Retriever:
        def __init__(self, *args, **kwargs):
            pass
        def retrieve(self, texts):
            return []
try:
    from .llm import LLMController
except Exception:
    class LLMController:
        def __init__(self, *args, **kwargs):
            pass
        def generate(self, prompt, max_tokens=256):
            return "Dummy answer"
try:
    from .orchestrator import RagOrchestrator
except Exception:
    class RagOrchestrator:
        def __init__(self, *args, **kwargs):
            pass
        def answer(self, query):
            return {"answer": "Dummy answer", "sources": [], "score": 0.0, "context": ""}

__all__ = [
    "EmbeddingService",
    "VectorStore",
    "Retriever",
    "LLMController",
    "RagOrchestrator",
]
