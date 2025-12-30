#!/usr/bin/env python3
"""
Quick test of ChromaDB basic functionality.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb

print("=== Testing ChromaDB ===")

# Test 1: Create client
print("\n[Test 1] Creating ChromaDB client...")
client = chromadb.PersistentClient(path="./data/chroma_quick_test")
print("✓ Client created")

# Test 2: Create collection
print("\n[Test 2] Creating collection...")
collection = client.get_or_create_collection(
    name="test_collection",
    metadata={"hnsw:space": "cosine"}
)
print("✓ Collection created")

# Test 3: Add documents
print("\n[Test 3] Adding documents...")
collection.add(
    documents=["Test doc 1", "Test doc 2", "Test doc 3"],
    metadatas=[
        {"source": "test1.txt", "type": "doc"},
        {"source": "test2.txt", "type": "code"},
        {"source": "test3.txt", "type": "doc"}
    ],
    ids=["doc_1", "doc_2", "doc_3"]
)
print("✓ Added 3 documents")

# Test 4: Get count
print("\n[Test 4] Getting count...")
count = collection.count()
print(f"✓ Collection has {count} documents")
assert count == 3, f"Expected 3 documents, got {count}"

# Test 5: Query with filter
print("\n[Test 5] Querying with metadata filter...")
results = collection.query(
    query_texts=["test"],
    n_results=10,
    where={"type": "doc"}
)
print(f"✓ Found {len(results['ids'][0])} results with type='doc'")
assert len(results['ids'][0]) == 2, f"Expected 2 results, got {len(results['ids'][0])}"

# Test 6: Delete collection
print("\n[Test 6] Deleting collection...")
client.delete_collection("test_collection")
print("✓ Collection deleted")

# Test 7: Verify deletion
print("\n[Test 7] Verifying deletion...")
collections = client.list_collections()
print(f"✓ Collections after deletion: {len(collections)}")
assert len(collections) == 0, f"Expected 0 collections, got {len(collections)}"

# Cleanup
print("\n[Cleanup] Removing test directory...")
import shutil
if os.path.exists("./data/chroma_quick_test"):
    shutil.rmtree("./data/chroma_quick_test")
print("✓ Test directory removed")

print("\n" + "="*50)
print("✓ All ChromaDB tests passed!")
print("="*50)
