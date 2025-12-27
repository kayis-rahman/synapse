"""
Simple example of the VectorStore component.
Stores and retrieves documents with vector embeddings.
"""

import numpy as np
from typing import List, Dict, Any


class SimpleVectorStore:
    """
    Minimal vector store implementation.
    Stores documents and vectors, performs cosine similarity search.
    """
    
    def __init__(self):
        self.docs: List[str] = []
        self.vectors: List[List[float]] = []
        self.metadata: List[Dict[str, Any]] = []
    
    def add(self, docs: List[str], vectors: List[List[float]], metadata: List[Dict[str, Any]] = None):
        """Add documents to the store."""
        if len(docs) != len(vectors):
            raise ValueError(f"docs and vectors length mismatch: {len(docs)} vs {len(vectors)}")
        
        self.docs.extend(docs)
        self.vectors.extend(vectors)
        
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{} for _ in docs])
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)
    
    def search(self, query_vector: List[float], top_k: int = 3) -> List[tuple]:
        """Search for top-k most similar documents."""
        if not self.vectors:
            return []
        
        scores = []
        for idx, vec in enumerate(self.vectors):
            score = self._cosine_similarity(query_vector, vec)
            scores.append((idx, score))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k results
        results = []
        for idx, score in scores[:top_k]:
            results.append((self.docs[idx], score, self.metadata[idx]))
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get store statistics."""
        return {
            "total_docs": len(self.docs),
            "total_vectors": len(self.vectors),
            "vector_dimension": len(self.vectors[0]) if self.vectors else 0
        }


def main():
    """Demonstrate SimpleVectorStore usage."""
    
    # Create store
    store = SimpleVectorStore()
    
    # Add sample documents
    docs = [
        "Python is a high-level programming language.",
        "FastAPI is a modern, fast web framework for building APIs.",
        "Machine learning is a subset of artificial intelligence.",
        "Docker is a platform for developing and deploying applications."
    ]
    
    vectors = [
        [0.1, 0.2, 0.3, 0.4],
        [0.2, 0.3, 0.4, 0.5],
        [0.3, 0.4, 0.5, 0.6],
        [0.4, 0.5, 0.6, 0.7]
    ]
    
    metadata = [
        {"topic": "programming", "language": "python"},
        {"topic": "web", "framework": "fastapi"},
        {"topic": "ai", "type": "machine learning"},
        {"topic": "devops", "tool": "docker"}
    ]
    
    store.add(docs, vectors, metadata)
    
    # Search for similar documents
    query_vector = [0.15, 0.25, 0.35, 0.45]
    results = store.search(query_vector, top_k=3)
    
    print("Vector Store Demo")
    print("=" * 60)
    print("\nQuery Vector:", query_vector)
    print("\nTop 3 Results:")
    for i, (doc, score, meta) in enumerate(results, 1):
        print(f"\n[{i}] Score: {score:.4f}")
        print(f"    Document: {doc}")
        print(f"    Metadata: {meta}")
    
    # Show stats
    stats = store.get_stats()
    print("\n" + "=" * 60)
    print("Store Statistics:")
    print(f"  Total documents: {stats['total_docs']}")
    print(f"  Total vectors: {stats['total_vectors']}")
    print(f"  Vector dimension: {stats['vector_dimension']}")


if __name__ == "__main__":
    main()
