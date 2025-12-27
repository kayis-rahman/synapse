"""
Comprehensive test suite for pi-rag RAG system.
Tests all components without requiring MLX server to be running.
"""

import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.vectorstore import VectorStore
from rag.embedding import EmbeddingService


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def record_pass(self, test_name):
        self.passed += 1
        print(f"✓ {test_name}")

    def record_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, str(error)))
        print(f"✗ {test_name}")
        print(f"  Error: {error}")

    def print_summary(self):
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        
        if self.errors:
            print("\nFailed Tests:")
            for test_name, error in self.errors:
                print(f"  - {test_name}")
                print(f"    {error}")
        
        print("=" * 60)


async def test_vectorstore_add():
    """Test VectorStore add operation."""
    store = VectorStore(":memory:")
    
    docs = ["Test doc 1", "Test doc 2"]
    vectors = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    metadata = [{"source": "test1"}, {"source": "test2"}]
    
    store.add(docs, vectors, metadata)
    
    assert len(store.docs) == 2
    assert len(store.vectors) == 2
    assert len(store.metadata) == 2
    
    return True


async def test_vectorstore_search():
    """Test VectorStore search operation."""
    store = VectorStore(":memory:")
    
    docs = ["Python programming", "FastAPI web framework", "Machine learning", "Docker containers"]
    vectors = [
        [0.1, 0.2, 0.3],  # Python
        [0.2, 0.3, 0.4],  # FastAPI
        [0.3, 0.4, 0.5],  # ML
        [0.4, 0.5, 0.6]   # Docker
    ]
    metadata = [{"topic": "python"}, {"topic": "web"}, {"topic": "ml"}, {"topic": "devops"}]
    
    store.add(docs, vectors, metadata)
    
    # Search for "Python programming"
    results = store.search([0.1, 0.2, 0.3], top_k=2)
    
    assert len(results) == 2
    assert "Python" in results[0][0]  # Should find Python doc first
    
    return True


async def test_vectorstore_metadata_filter():
    """Test VectorStore metadata filtering."""
    store = VectorStore(":memory:")
    
    docs = ["Doc 1", "Doc 2", "Doc 3"]
    vectors = [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]]
    metadata = [
        {"project": "pi-rag", "service": "rag"},
        {"project": "other", "service": "api"},
        {"project": "pi-rag", "service": "vector"}
    ]
    
    store.add(docs, vectors, metadata)
    
    # Search with project filter
    results = store.search([0.1, 0.2], top_k=10, metadata_filters={"project": "pi-rag"})
    
    assert len(results) == 2  # Should only find pi-rag docs
    
    return True


async def test_vectorstore_persistence():
    """Test VectorStore save/load persistence."""
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        store1 = VectorStore(tmpdir)
        
        docs = ["Persistent document"]
        vectors = [[0.1, 0.2, 0.3]]
        metadata = [{"source": "test"}]
        
        store1.add(docs, vectors, metadata)
        store1.save()
        
        # Load into new instance
        store2 = VectorStore(tmpdir)
        
        assert len(store2.docs) == 1
        assert store2.docs[0] == "Persistent document"
        assert store2.metadata[0]["source"] == "test"
    
    return True


async def test_vectorstore_clear():
    """Test VectorStore clear operation."""
    store = VectorStore(":memory:")
    
    store.add(["doc"], [[0.1, 0.2]], [{"source": "test"}])
    assert len(store.docs) == 1
    
    store.clear()
    
    assert len(store.docs) == 0
    assert len(store.vectors) == 0
    assert len(store.metadata) == 0
    
    return True


async def test_vectorstore_stats():
    """Test VectorStore get_stats operation."""
    store = VectorStore(":memory:")
    
    docs = ["Doc 1", "Doc 2"]
    vectors = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    metadata = [{"source": "test1"}, {"source": "test2"}]
    
    store.add(docs, vectors, metadata)
    
    stats = store.get_stats()
    
    assert stats["total_docs"] == 2
    assert stats["total_vectors"] == 2
    assert stats["vector_dimension"] == 3
    
    return True


async def test_embedding_service_init():
    """Test EmbeddingService initialization."""
    service = EmbeddingService(
        mlx_server_url="http://localhost:8000",
        embedding_model="mlx-community/all-MiniLM-L6-v2-4bit",
        cache_enabled=True,
        cache_size=1000
    )
    
    assert service.mlx_server_url == "http://localhost:8000"
    assert service.embedding_model == "mlx-community/all-MiniLM-L6-v2-4bit"
    assert service.cache_enabled == True
    assert service.cache_size == 1000
    
    await service.close()
    return True


async def test_embedding_cache_stats():
    """Test EmbeddingService cache statistics."""
    service = EmbeddingService(
        mlx_server_url="http://localhost:8000",
        embedding_model="mlx-community/all-MiniLM-L6-v2-4bit",
        cache_enabled=True,
        cache_size=1000
    )
    
    stats = service.get_cache_stats()
    
    assert "cache_enabled" in stats
    assert "cache_size" in stats
    assert "cache_size" in stats  # or "cache_entries" based on implementation
    assert stats["cache_enabled"] == True
    assert stats["cache_size"] == 1000
    
    await service.close()
    return True


async def test_embedding_cache_clear():
    """Test EmbeddingService cache clearing."""
    service = EmbeddingService(
        mlx_server_url="http://localhost:8000",
        embedding_model="mlx-community/all-MiniLM-L6-v2-4bit",
        cache_enabled=True,
        cache_size=1000
    )
    
    service.clear_cache()
    
    stats = service.get_cache_stats()
    assert stats["cache_size"] == 0 or stats.get("cache_entries", 0) == 0
    
    await service.close()
    return True


async def run_tests():
    """Run all tests."""
    results = TestResults()
    
    print("=" * 60)
    print("pi-rag RAG Component Tests")
    print("=" * 60)
    print()
    
    # VectorStore Tests
    print("Testing VectorStore...")
    print("-" * 60)
    
    tests = [
        ("Add documents", test_vectorstore_add),
        ("Search documents", test_vectorstore_search),
        ("Metadata filtering", test_vectorstore_metadata_filter),
        ("Persistence", test_vectorstore_persistence),
        ("Clear", test_vectorstore_clear),
        ("Get stats", test_vectorstore_stats)
    ]
    
    for test_name, test_func in tests:
        try:
            await test_func()
            results.record_pass(f"VectorStore: {test_name}")
        except Exception as e:
            results.record_fail(f"VectorStore: {test_name}", e)
    
    print()
    
    # EmbeddingService Tests
    print("Testing EmbeddingService...")
    print("-" * 60)
    
    embedding_tests = [
        ("Initialization", test_embedding_service_init),
        ("Cache statistics", test_embedding_cache_stats),
        ("Cache clear", test_embedding_cache_clear)
    ]
    
    for test_name, test_func in embedding_tests:
        try:
            await test_func()
            results.record_pass(f"EmbeddingService: {test_name}")
        except Exception as e:
            results.record_fail(f"EmbeddingService: {test_name}", e)
    
    # Print summary
    results.print_summary()
    
    # Return exit code
    return 0 if results.failed == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_tests())
    sys.exit(exit_code)
