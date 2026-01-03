#!/usr/bin/env python3
"""
Performance Baseline Benchmark

Measures current system performance across multiple categories.
"""

import json
import time
import psutil
from typing import List, Dict, Any
from rag.semantic_retriever import SemanticRetriever
from rag.semantic_ingest import SemanticIngestor
from rag.memory_store import MemoryStore
from rag.semantic_store import SemanticStore


def measure_memory_usage() -> Dict[str, Any]:
    """Measure current memory and cache usage."""
    process = psutil.Process()

    return {
        "rss_mb": process.memory_info().rss / 1024 / 1024,
        "vms_mb": process.memory_info().vms / 1024 / 1024,
    }


def get_total_chunk_count() -> int:
    """Get total chunk count from semantic store."""
    try:
        from rag.semantic_store import SemanticStore
        store = SemanticStore()
        return len(store.chunks)
    except:
        return 0


def get_cache_stats() -> Dict[str, Any]:
    """Get embedding cache statistics."""
    try:
        from rag.embedding import EmbeddingService
        service = EmbeddingService()
        return service.get_cache_stats()
    except:
        return {
            "cache_hits": 0,
            "cache_misses": 0,
            "cache_hit_rate": 0.0
        }


def get_database_performance() -> Dict[str, Any]:
    """Measure database performance."""
    import sqlite3
    import os

    # Check semantic store database
    semantic_db = "/opt/pi-rag/data/semantic_index/chroma.sqlite3"
    db_stats = {"semantic_db_exists": False, "semantic_db_size_mb": 0}

    if os.path.exists(semantic_db):
        db_stats["semantic_db_exists"] = True
        db_stats["semantic_db_size_mb"] = os.path.getsize(semantic_db) / 1024 / 1024

    # Check symbolic memory database
    symbolic_db = "/opt/pi-rag/data/memory.db"
    if os.path.exists(symbolic_db):
        try:
            conn = sqlite3.connect(symbolic_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory_facts")
            fact_count = cursor.fetchone()[0]
            conn.close()
            db_stats["symbolic_fact_count"] = fact_count
            db_stats["symbolic_db_size_mb"] = os.path.getsize(symbolic_db) / 1024 / 1024
        except Exception as e:
            db_stats["symbolic_db_error"] = str(e)

    # Check episodic memory database
    episodic_db = "/opt/pi-rag/data/episodic.db"
    if os.path.exists(episodic_db):
        try:
            conn = sqlite3.connect(episodic_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM episodes")
            episode_count = cursor.fetchone()[0]
            conn.close()
            db_stats["episodic_episode_count"] = episode_count
            db_stats["episodic_db_size_mb"] = os.path.getsize(episodic_db) / 1024 / 1024
        except Exception as e:
            db_stats["episodic_db_error"] = str(e)

    return db_stats


def baseline_query_performance(num_queries: int = 100) -> Dict[str, Any]:
    """Measure query performance baseline."""
    print(f"\n{'='*60}")
    print(f"Query Performance Benchmark")
    print(f"{'='*60}")
    print(f"Testing {num_queries} queries...")
    print(f"{'='*60}")

    from rag.semantic_retriever import SemanticRetriever
    retriever = SemanticRetriever()

    test_queries = [
        "RAG orchestrator implementation",
        "semantic memory chunking",
        "embedding model configuration",
        "symbolic memory facts",
        "MCP server tools",
        "chroma vector store",
        "retrieval configuration",
    ]

    # Add variations for testing
    variations = [
        "RAG orchestrator",
        "How does the RAG orchestrator work?",
        "What is the RAG orchestrator implementation?",
        "RAG orchestrator implementation details"
    ]

    query_times = []
    result_counts = []

    for i, query in enumerate(test_queries):
        start = time.perf_counter()
        results = retriever.retrieve(query, top_k=3)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        query_times.append(elapsed)
        result_counts.append(len(results))

        if (i + 1) % 20 == 0:
            print(f"Progress: {i+1}/{len(test_queries)} queries ({(i+1)/len(test_queries)*100:.0f}%)")

    # Calculate metrics
    query_times_sorted = sorted(query_times)

    metrics = {
        "avg_ms": sum(query_times) / len(query_times),
        "p50_ms": query_times_sorted[len(query_times_sorted) // 2],
        "p95_ms": query_times_sorted[int(len(query_times_sorted) * 0.95)],
        "p99_ms": query_times_sorted[int(len(query_times_sorted) * 0.99)],
        "min_ms": min(query_times),
        "max_ms": max(query_times),
        "total_queries": len(test_queries),
        "avg_results": sum(result_counts) / len(result_counts)
    }

    print(f"\nQuery Performance Results:")
    print(f"  Average: {metrics['avg_ms']:.0f}ms")
    print(f"  P50: {metrics['p50_ms']:.0f}ms")
    print(f"  P95: {metrics['p95_ms']:.0f}ms")
    print(f"  P99: {metrics['p99_ms']:.0f}ms")
    print(f"  Min: {metrics['min_ms']:.0f}ms")
    print(f"  Max: {metrics['max_ms']:.0f}ms")

    return metrics


def baseline_ingestion_performance() -> Dict[str, Any]:
    """Measure ingestion performance for various file sizes."""
    print(f"\n{'='*60}")
    print(f"Ingestion Performance Benchmark")
    print(f"{'='*60}")
    print("Testing ingestion for various file sizes...")
    print(f"{'='*60}")

    from rag.semantic_ingest import SemanticIngestor
    import tempfile
    import os

    ingestor = SemanticIngestor()

    # Create test files of different sizes
    file_sizes = [1000, 5000, 10000, 50000]  # lines
    ingestion_times = {}

    for size in file_sizes:
        print(f"\nTesting file size: {size} lines")

        # Create test file
        content = "\n".join([f"Line {i}: Test content for line {i}" for i in range(size)])

        # Measure ingestion time (run 3 times for avg)
        times = []
        chunks_created = []

        for run in range(3):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(content)
                temp_path = f.name

            start = time.perf_counter()
            try:
                chunk_ids = ingestor.ingest_file(
                    file_path=temp_path,
                    metadata={"test_file": True, "size": size}
                )
                chunks_created.append(len(chunk_ids))
                elapsed = (time.perf_counter() - start) * 1000  # ms
                times.append(elapsed)
            finally:
                os.unlink(temp_path)

        avg_time = sum(times) / len(times)
        avg_chunks = sum(chunks_created) / len(chunks_created)

        ingestion_times[f"size_{size}"] = {
            "avg_time_ms": avg_time,
            "chunks_per_ms": size / avg_time if avg_time > 0 else 0,
            "avg_chunks": avg_chunks
        }

        print(f"  Average time: {avg_time:.0f}ms")
        print(f"  Average chunks: {avg_chunks}")
        print(f"  Speed: {size / avg_time if avg_time > 0 else 0:.1f} lines/ms")

    # Calculate metrics
    metrics = {}
    for size_key, data in ingestion_times.items():
        metrics[size_key] = data

    return metrics


def baseline_embedding_performance(num_embeddings: int = 100) -> Dict[str, Any]:
    """Measure embedding generation performance."""
    print(f"\n{'='*60}")
    print(f"Embedding Generation Benchmark")
    print(f"{'='*60}")
    print(f"Generating {num_embeddings} embeddings...")
    print(f"{'='*60}")

    from rag.embedding import EmbeddingService

    embedding_service = EmbeddingService()

    # Generate embeddings for texts of different lengths
    text_lengths = [100, 300, 500, 700, 1000]  # characters

    embedding_times = {}

    for length in text_lengths:
        print(f"\nTesting text length: {length} characters")

        times = []
        for _ in range(num_embeddings // 5):  # 20 tests per length
            text = "a" * length  # Simple text

            start = time.perf_counter()
            try:
                embedding = embedding_service.get_embedding(text)
                elapsed = (time.perf_counter() - start) * 1000  # ms
                times.append(elapsed)
            except Exception as e:
                print(f"  Error: {e}")
                continue

        avg_time = sum(times) / len(times) if times else 0

        embedding_times[f"length_{length}"] = {
            "avg_ms": avg_time,
            "embeddings_per_sec": 1000 / avg_time if avg_time > 0 else 0,
            "num_tests": len(times)
        }

        print(f"  Average time: {avg_time:.0f}ms")
        print(f"  Speed: {1000 / avg_time if avg_time > 0 else 0:.1f} embeddings/sec")

    return embedding_times


def main():
    """Run baseline performance benchmark."""
    print("=" * 70)
    print("Performance Baseline Benchmark")
    print("=" * 70)
    print()

    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "memory_usage": measure_memory_usage(),
        "cache_stats": get_cache_stats(),
        "database_performance": get_database_performance(),
    }

    # Query performance benchmark
    print("\n" + "="*70)
    results["query_performance"] = baseline_query_performance()

    # Ingestion performance benchmark
    results["ingestion_performance"] = baseline_ingestion_performance()

    # Embedding performance benchmark
    results["embedding_performance"] = baseline_embedding_performance()

    # Save results
    output_file = "/opt/pi-rag/data/baseline_performance_metrics.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print()
    print("=" * 70)
    print("Baseline Benchmark Complete")
    print("=" * 70)
    print()
    print(f"Results saved to: {output_file}")

    # Print summary
    print()
    print("Summary:")
    print(f"  Query Performance:")
    print(f"    Average: {results['query_performance']['avg_ms']:.0f}ms")
    print(f"    P50: {results['query_performance']['p50_ms']:.0f}ms")
    print(f"    P95: {results['query_performance']['p95_ms']:.0f}ms")
    print()
    print(f"  Ingestion Performance:")
    sizes_tested = list(results['ingestion_performance'].keys())
    print(f"    Tested sizes: {sizes_tested}")
    print()
    print(f"  Embedding Performance:")
    lengths_tested = list(results['embedding_performance'].keys())
    print(f"    Tested lengths: {lengths_tested}")
    print()
    print(f"  Memory Usage:")
    print(f"    RSS: {results['memory_usage']['rss_mb']:.1f}MB")
    print(f"    VMS: {results['memory_usage']['vms_mb']:.1f}MB")
    print()
    print(f"  Cache Stats:")
    print(f"    Hit Rate: {results['cache_stats'].get('cache_hit_rate', 0):.1%}")
    print()
    print(f"  Database:")
    print(f"    Semantic DB: {results['database_performance'].get('semantic_db_size_mb', 0):.2f}MB")
    print(f"    Symbolic DB: {results['database_performance'].get('symbolic_db_size_mb', 0):.2f}MB")
    print(f"    Episodic DB: {results['database_performance'].get('episodic_db_size_mb', 0):.2f}MB")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
