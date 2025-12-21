from typing import List


class RagOrchestrator:
    def __init__(self, embedding_service, vector_store, retriever, llm_controller, top_k: int = 5):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.retriever = retriever
        self.llm_controller = llm_controller
        self.top_k = top_k

    def answer(self, query: str, model=None, temperature=0.7, api_key=None) -> dict:
        # Embed the query
        q_vecs = self.embedding_service.embed([query])
        query_vec = q_vecs[0] if q_vecs else []
        # Retrieve candidates
        results = self.vector_store.search(query_vec, top_k=self.top_k) if self.vector_store else []
        docs = [d for d, _score, _md in results]
        context = "\n---\n".join(docs) if docs else ""
        prompt = f"Question: {query}\nContext:\n{context}\n"
        # Generate answer using LLM
        answer = self.llm_controller.generate(prompt, model=model, temperature=temperature, api_key=api_key)
        score = max((s for _d, s, _md in results), default=0.0) if results else 0.0
        return {
            "answer": answer,
            "sources": docs,
            "score": score,
            "context": context,
        }
