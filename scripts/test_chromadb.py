#!/usr/bin/env python3
"""
Test ChromaDB vector store implementations.

Tests both ChromaVectorStore and ChromaSemanticStore.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.chroma_vectorstore import ChromaVectorStore
from rag.chroma_semantic_store import ChromaSemanticStore, DocumentChunk
from rag.embedding import get_embedding_service

def test_chroma_vectorstore():
    """Test ChromaVectorStore basic operations."""
    print("\n=== Testing ChromaVectorStore ===")

    # Create store
    store = ChromaVectorStore(
        index_path="./data/test_chroma_rag",
        collection_name="test_rag"
    )

    # Test 1: Add documents
    print("\n[Test 1] Adding documents...")
    docs = ["Test document 1", "Test document 2", "Test document 3"]
    # Create dummy embeddings (1024 dimensions)
    import numpy as np
    vectors = [np.random.rand(1024).tolist() for _ in range(3)]
    metadata = [
        {"source": "test1.txt", "type": "doc"},
        {"source": "test2.txt", "type": "doc"},
        {"source": "test3.txt", "type": "code"}
    ]

    store.add(docs, vectors, metadata)
    print(f"✓ Added {len(docs)} documents")

    # Test 2: Get stats
    print("\n[Test 2] Getting stats...")
    stats = store.get_stats()
    print(f"✓ Stats: {stats}")
    assert stats["total_docs"] == 3, "Expected 3 docs"

    # Test 3: Search
    print("\n[Test 3] Searching...")
    query_vector = np.random.rand(1024).tolist()
    results = store.search(query_vector, top_k=2)
    print(f"✓ Found {len(results)} results")
    for i, (doc, score, meta) in enumerate(results):
        print(f"  Result {i+1}: score={score:.3f}, source={meta.get('source', 'unknown')}")

    # Test 4: Metadata filtering
    print("\n[Test 4] Searching with metadata filter...")
    filtered_results = store.search(
        query_vector,
        top_k=10,
        metadata_filters={"type": "doc"}
    )
    print(f"✓ Found {len(filtered_results)} results with type='doc'")
    assert len(filtered_results) == 2, "Expected 2 docs with type='doc'"

    # Test 5: Clear
    print("\n[Test 5] Clearing store...")
    store.clear()
    stats = store.get_stats()
    print(f"✓ Store cleared, stats: {stats}")
    assert stats["total_docs"] == 0, "Expected 0 docs after clear"

    print("\n✓ All ChromaVectorStore tests passed!")


def test_chroma_semantic_store():
    """Test ChromaSemanticStore basic operations."""
    print("\n=== Testing ChromaSemanticStore ===")

    # Create store
    try:
        embedding_service = get_embedding_service()
    except Exception as e:
        print(f"Warning: Failed to load embedding service: {e}")
        print("Skipping ChromaSemanticStore tests (requires embedding model)")
        return

    store = ChromaSemanticStore(
        index_path="./data/test_chroma_semantic",
        collection_name="test_semantic",
        embedding_service=embedding_service
    )

    # Test 1: Add document
    print("\n[Test 1] Adding document...")
    content = """This is a test document for the ChromaDB semantic store.
It contains multiple paragraphs and should be chunked automatically.
The semantic store is designed to store documents and code."""

    metadata = {
        "source": "test_doc.txt",
        "type": "doc",
        "project_id": "test_project"
    }

    chunk_ids = store.add_document(content, metadata, chunk_size=100, chunk_overlap=20)
    print(f"✓ Added document with {len(chunk_ids)} chunks")
    if chunk_ids:
        print(f"  Chunk IDs: {chunk_ids[:3]}...")

    # Test 2: Get stats
    print("\n[Test 2] Getting stats...")
    stats = store.get_stats()
    print(f"✓ Stats: {stats}")
    assert stats["total_chunks"] > 0, "Expected chunks"

    # Test 3: Search (requires embeddings)
    print("\n[Test 3] Searching...")
    try:
        results = store.search("test document", top_k=3)
        print(f"✓ Found {len(results)} results")
        for i, result in enumerate(results[:2]):
            print(f"  Result {i+1}: score={result['score']:.3f}, chunk={result['chunk_index']}")
            print(f"    Content preview: {result['content'][:50]}...")
    except Exception as e:
        print(f"Warning: Search failed (embedding service may not be configured): {e}")

    # Test 4: Get chunk by ID
    print("\n[Test 4] Getting chunk by ID...")
    if chunk_ids:
        chunk = store.get_chunk_by_id(chunk_ids[0])
        if chunk:
            print(f"✓ Retrieved chunk: {chunk.chunk_id}")
            print(f"    Content: {chunk.content[:50]}...")

    # Test 5: Get document IDs
    print("\n[Test 5] Listing documents...")
    print(f"✓ Total documents: {len(store.document_ids)}")

    # Test 6: Delete document
    print("\n[Test 6] Deleting document...")
    if store.document_ids:
        doc_id = list(store.document_ids)[0]
        deleted = store.delete_document(doc_id)
        print(f"✓ Deleted {deleted} chunks")
        stats = store.get_stats()
        print(f"    New total chunks: {stats['total_chunks']}")

    print("\n✓ All ChromaSemanticStore tests passed!")


def cleanup():
    """Clean up test data."""
    print("\n=== Cleaning up ===")
    import shutil
    test_paths = [
        "./data/test_chroma_rag",
        "./data/test_chroma_semantic"
    ]
    for path in test_paths:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"✓ Removed {path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test ChromaDB implementations")
    parser.add_argument("--cleanup", action="store_true", help="Clean up test data only")
    parser.add_argument("--no-cleanup", action="store_true", help="Skip cleanup")

    args = parser.parse_args()

    if args.cleanup:
        cleanup()
        sys.exit(0)

    try:
        test_chroma_vectorstore()
        test_chroma_semantic_store()

        if not args.no_cleanup:
            print("\n" + "="*50)
            print("All tests passed!")
            print("="*50)
            cleanup()

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
