from __future__ import division

class Retriever:
    def __init__(self, embedding_service, vector_store, top_k=5):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, texts):
        if not texts:
            return []
        embeddings = self.embedding_service.embed(texts)
        query_vec = embeddings[0]
        if len(embeddings) > 1:
            dim = len(embeddings[0])
            query_vec = [sum(vec[i] for vec in embeddings) / len(embeddings) for i in range(dim)]
        return self.vector_store.search(query_vec, top_k=self.top_k)
