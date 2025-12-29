"""
Example Usage of Phase 4: Semantic Memory (RAG)

This script demonstrates how to:
1. Ingest documents and code into semantic memory
2. Retrieve relevant documents with rankings
3. Inject semantic context as non-authoritative information
4. Combine with symbolic and episodic memory

Run this script to see semantic memory in action.
"""

import tempfile
from typing import Dict, Any, List

# Import semantic memory components
from rag.semantic_store import SemanticStore, DocumentChunk, get_semantic_store
from rag.semantic_ingest import SemanticIngestor, get_semantic_ingestor
from rag.semantic_retriever import SemanticRetriever, get_semantic_retriever
from rag.semantic_injector import SemanticInjector, get_semantic_injector


def example_1_basic_ingestion():
    """Example 1: Basic document ingestion."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Document Ingestion")
    print("="*70)

    # Create temporary index
    index_path = tempfile.mktemp(suffix="_semantic_index")

    # Create ingestor
    ingestor = get_semantic_ingestor()

    # Ingest a sample document
    sample_doc = """
    # API Documentation

    ## Authentication

    The system uses JWT tokens for authentication.

    ## Authorization

    Users must have appropriate permissions to access resources.
    """

    # Ingest with metadata
    chunk_ids = ingestor.ingest_text(
        text=sample_doc,
        metadata={
            "type": "doc",
            "source": "docs/api.md",
            "title": "API Documentation"
        }
    )

    print(f"\n✓ Ingested document: {len(chunk_ids)} chunks created")

    # Get stats
    store = get_semantic_store(index_path)
    stats = store.get_stats()

    print(f"\nStatistics:")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Total documents: {stats['total_documents']}")
    print(f"  By type: {stats.get('by_type', {})}")

    # Clean up
    import os
    import shutil
    if os.path.exists(index_path):
        shutil.rmtree(index_path)


def example_2_query_driven_retrieval():
    """Example 2: Query-driven retrieval (not automatic)."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Query-Driven Retrieval")
    print("="*70)

    # Create temporary index
    index_path = tempfile.mktemp(suffix="_semantic_index")

    # Create ingestor and retriever
    ingestor = get_semantic_ingestor(semantic_store=None)
    retriever = get_semantic_retriever(semantic_store=None, embedding_service=None)

    # Ingest sample documents
    docs = [
        ("API uses JWT for authentication.", {"type": "doc", "source": "docs/api.md"}),
        ("User class handles login logic.", {"type": "code", "source": "auth.py"}),
        ("README describes project setup.", {"type": "doc", "source": "README.md"}),
    ]

    for i, (content, metadata) in enumerate(docs):
        ingestor.semantic_store = get_semantic_store(index_path)
        ingestor.ingest_text(
            text=content,
            metadata={
                **metadata,
                "document_id": f"doc_{i}"
            }
        )

    print(f"\n✓ Ingested {len(docs)} documents")

    # Simulate planner requesting retrieval (query-driven, not automatic)
    query = "How does authentication work?"

    print(f"\n--- PLANNER REQUEST ---")
    print(f"Planner checks: Symbolic memory cannot answer '{query}'")
    print(f"Planner decides: Need external information")
    print(f"Planner triggers: Retrieval (query-driven)")
    print(f"--------------------------")

    # Retrieve (with valid trigger)
    try:
        results = retriever.retrieve(
            query=query,
            trigger="external_info_needed",
            top_k=3
        )

        print(f"\n✓ Retrieved {len(results)} results")

        for i, result in enumerate(results, 1):
            print(f"\n  Result {i}:")
            print(f"    Content: {result['content'][:100]}...")
            print(f"    Score: {result['score']:.3f}")
            print(f"    Citation: {result['citation']}")
            print(f"    Source: {result['metadata'].get('source', 'unknown')}")
    except ValueError as e:
        print(f"\n✗ Retrieval blocked: {e}")

    # Clean up
    import os
    import shutil
    if os.path.exists(index_path):
        shutil.rmtree(index_path)


def example_3_metadata_filtering():
    """Example 3: Filtering by metadata (type, source)."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Metadata Filtering")
    print("="*70)

    # Create temporary index
    index_path = tempfile.mktemp(suffix="_semantic_index")

    # Create ingestor and retriever
    ingestor = get_semantic_ingestor(semantic_store=None)
    retriever = get_semantic_retriever(semantic_store=None, embedding_service=None)

    # Ingest documents with different types
    docs = [
        ("API authentication uses JWT.", {"type": "doc", "source": "docs/api.md"}),
        ("class AuthController { ... }", {"type": "code", "source": "auth.go"}),
        ("User settings configuration.", {"type": "note", "source": "config.json"}),
    ]

    for i, (content, metadata) in enumerate(docs):
        ingestor.semantic_store = get_semantic_store(index_path)
        ingestor.ingest_text(
            text=content,
            metadata={
                **metadata,
                "document_id": f"doc_{i}"
            }
        )

    print(f"\n✓ Ingested {len(docs)} documents with different types")

    # Filter by type (code only)
    code_results = retriever.search_by_type(
        query="How to authenticate?",
        doc_type="code",
        top_k=3
    )

    print(f"\n✓ Code-only results: {len(code_results)}")
    for result in code_results:
        print(f"    - {result['content'][:80]}...")

    # Filter by source (docs/api.md only)
    source_results = retriever.search_by_source(
        query="Authentication",
        source_pattern="docs/api.md",
        top_k=2
    )

    print(f"\n✓ Source-specific results: {len(source_results)}")
    for result in source_results:
        print(f"    - {result['content'][:80]}...")

    # Clean up
    import os
    import shutil
    if os.path.exists(index_path):
        shutil.rmtree(index_path)


def example_4_non_authoritative_injection():
    """Example 4: Non-authoritative context injection."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Non-Authoritative Context Injection")
    print("="*70)

    injector = get_semantic_injector()

    # Mock retrieval results
    results = [
        {
            "content": "API authentication uses JWT tokens for secure access.",
            "score": 0.92,
            "citation": "docs/api.md:0",
            "metadata": {
                "source": "docs/api.md",
                "type": "doc",
                "document_id": "doc_api_docs"
            }
        },
        {
            "content": "AuthController class handles login and token validation.",
            "score": 0.88,
            "citation": "auth.go:2",
            "metadata": {
                "source": "auth.go",
                "type": "code",
                "document_id": "doc_auth_go"
            }
        }
    ]

    # Inject as non-authoritative context
    injected = injector.inject_context(
        query="How does authentication work?",
        results=results,
        include_citations=True,
        include_scores=True
    )

    print(f"\nInjected Context:")
    print(injected)

    # Verify non-authoritative markers
    print(f"\n✓ Contains 'NON-AUTHORITATIVE': {'NON-AUTHORITATIVE' in injected}")
    print(f"✓ Contains disclaimer: {'Note:' in injected and 'not verified' in injected}")
    print(f"✓ Contains citations: {'citation' in injected}")


def example_5_combined_memory_types():
    """Example 5: Combining symbolic, episodic, and semantic memory."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Combined Memory Types")
    print("="*70)

    injector = get_semantic_injector()

    # Mock contexts from all memory types
    symbolic_context = """
PERSISTENT MEMORY (READ-ONLY):
• Project language: Go (confidence 0.92)
• User prefers JSON output (confidence 0.85)
"""

    episodic_context = """
PAST AGENT LESSONS (ADVISORY, NON-AUTHORITATIVE):
• For large repos, search filenames first (confidence 0.85)
• User prefers concise output (confidence 0.90)

Note: These are lessons from experience, not guaranteed facts.
"""

    semantic_results = [
        {
            "content": "API documentation describes JWT authentication flow.",
            "score": 0.91,
            "citation": "docs/api.md:1",
            "metadata": {"source": "docs/api.md", "type": "doc"}
        }
    ]

    # Inject combined context
    query = "How does API authentication work?"

    combined = injector.inject_with_memory_context(
        query=query,
        semantic_results=semantic_results,
        symbolic_context=symbolic_context,
        episodic_context=episodic_context
    )

    print(f"\nQuery: {query}")
    print(f"\nCombined Context:")
    print(combined)

    # Verify proper ordering
    print(f"\n✓ Symbolic memory comes FIRST: {'PERSISTENT MEMORY' in combined[:50]}")
    print(f"✓ Episodic memory comes SECOND: {'PAST AGENT LESSONS' in combined[100:200]}")
    print(f"✓ Semantic memory comes LAST: {'RETRIEVED CONTEXT' in combined[-100:]}")
    print(f"✓ Semantic is NON-AUTHORITATIVE: {'NON-AUTHORITATIVE' in combined}")


def example_6_retrieval_with_ranking():
    """Example 6: Retrieval with similarity, metadata, and recency ranking."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Retrieval with Ranking")
    print("="*70)

    # Create temporary index
    index_path = tempfile.mktemp(suffix="_semantic_index")

    # Create retriever
    retriever = get_semantic_retriever(semantic_store=None, embedding_service=None)

    # Mock some chunks with different recency
    from datetime import datetime, timedelta
    import json

    # We'll manually add chunks with timestamps
    # In production, this happens during ingestion

    print(f"\n✓ Simulated retrieval with ranking factors:")
    print(f"  - Similarity score (0.0-1.0)")
    print(f"  - Metadata relevance boost")
    print(f"  - Recency decay (recent documents boosted)")

    # Demonstrate ranking explanation
    results = [
        {
            "content": "JWT token authentication for API access.",
            "score": 0.95,
            "citation": "docs/api.md:0",
            "metadata": {"source": "docs/api.md", "type": "doc"},
            "ranking_factors": {
                "similarity": 0.95,
                "metadata": 0.0,
                "recency": 0.9
            }
        }
    ]

    # Explain ranking
    explanations = retriever.explain_ranking(results)

    print(f"\nRanking Explanations:")
    for exp in explanations:
        print(f"  {exp}")

    # Clean up
    import os
    if os.path.exists(index_path):
        os.rmdir(index_path)


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*10 + "PHASE 4: SEMANTIC MEMORY (RAG) - EXAMPLE USAGE" + " "*10 + "║")
    print("╚" + "="*68 + "╝")

    # Run examples
    example_1_basic_ingestion()
    example_2_query_driven_retrieval()
    example_3_metadata_filtering()
    example_4_non_authoritative_injection()
    example_5_combined_memory_types()
    example_6_retrieval_with_ranking()

    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70)
    print("\nKey Takeaways:")
    print("  ✓ Semantic memory stores DOCUMENTS and CODE, not preferences or facts")
    print("  ✓ Retrieval is QUERY-DRIVEN (not automatic)")
    print("  ✓ Retrieved content is NON-AUTHORITATIVE")
    print("  ✓ Citations provide source traceability")
    print("  ✓ Ranking combines similarity + metadata + recency")
    print("  ✓ Memory types are clearly separated (symbolic → episodic → semantic)")
    print("\nSee PHASE4_SEMANTIC_MEMORY.md for full documentation.\n")


if __name__ == "__main__":
    main()
