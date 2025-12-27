"""
Simple test script to verify RAG components work correctly.
"""

import asyncio
from rag.vectorstore import VectorStore
from rag.embedding import EmbeddingService


async def test_vectorstore():
    """Test VectorStore basic operations."""
    print("Testing VectorStore...")
    store = VectorStore(":memory:")
    
    docs = ["Test document 1", "Test document 2"]
    vectors = [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]]
    metadata = [{"source": "test1"}, {"source": "test2"}]
    
    store.add(docs, vectors, metadata)
    
    if len(store.docs) != 2:
        raise AssertionError(f"Expected 2 docs, got {len(store.docs)}")
    
    if len(store.vectors) != 2:
        raise AssertionError(f"Expected 2 vectors, got {len(store.vectors)}")
    
    if len(store.metadata) != 2:
        raise AssertionError(f"Expected 2 metadata, got {len(store.metadata)}")
    
    print("VectorStore test passed!")
    return True


async def test_embedding():
    """Test EmbeddingService without MLX server."""
    print("Testing EmbeddingService (without MLX server)...")
    
    service = EmbeddingService(
        mlx_server_url="http://localhost:8000",
        embedding_model="mlx-community/all-MiniLM-L6-v2-4bit",
        cache_enabled=True,
        cache_size=1000
    )
    
    stats = service.get_cache_stats()
    
    if not stats["cache_enabled"]:
        raise AssertionError(f"Expected cache enabled, got {stats['cache_enabled']}")
    
    if stats["cache_size"] != 1000:
        raise AssertionError(f"Expected cache size 1000, got {stats['cache_size']}")
    
    if stats["cache_entries"] != 0:
        raise AssertionError(f"Expected 0 cache entries, got {stats['cache_entries']}")
    
    print("EmbeddingService test passed!")
    return True


async def test_integration():
    """Test integration of all components."""
    print("Testing full integration...")
    
    service = EmbeddingService(
        mlx_server_url="http://localhost:8000",
        embedding_model="mlx-community/all-MiniLM-L6-v2-4bit",
        cache_enabled=True,
        cache_size=1000
    )
    
    store = VectorStore(":memory:")
    
    docs = ["Test doc about Python", "Test doc about FastAPI"]
    vectors = [[0.1, 0.2], [0.3, 0.4]]
    metadata = [{"type": "code"}, {"type": "docs"}]
    
    store.add(docs, vectors, metadata)
    
    query = "What is Python?"
    query_embeddings = await service.embed([query])
    results = store.search(query_embeddings[0], top_k=2)
    
    if len(results) != 2:
        raise AssertionError(f"Expected 2 results, got {len(results)}")
    
    await service.close()
    
    print("Integration test passed!")
    return True


async def main():
    print("=" * 60)
    print("RAG Component Tests")
    print("=" * 60)
    print()
    
    try:
        await test_vectorstore()
        print()
        
        await test_embedding()
        print()
        
        await test_integration()
        print()
        
        print("=" * 60)
        print("All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
