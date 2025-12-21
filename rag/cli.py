import sys
from .embedding import EmbeddingService
from .vectorstore import VectorStore
from .retriever import Retriever
from .llm import LLMController
from .orchestrator import RagOrchestrator


def main():
    # Simple CLI example: python -m rag.cli <query>
    if len(sys.argv) < 2:
        print("Usage: python -m rag.cli '<query>'")
        sys.exit(1)
    query = sys.argv[1]

    # Lightweight scaffolding using in-memory store
    emb = EmbeddingService()
    store = VectorStore(index_path=None)

    # Example docs
    docs = ["OpenRouter is a free, open API for LLMs.",
            "RAG combines embeddings and retrieval to provide context-aware answers.",
            "All-MiniLM-L6-v2 is a compact embedding model suitable for fast inference."]
    vecs = emb.embed(docs)
    store.add(docs, vecs, metadata=[{"source": "docs"}] * len(docs))
    store.save("/tmp/rag_index_example")

    retr = Retriever(emb, store, top_k=2)
    llm = LLMController()
    ort = RagOrchestrator(emb, store, retr, llm, top_k=2)
    answer = ort.answer(query)
    print("Answer:\n" + str(answer))


if __name__ == '__main__':
    main()
