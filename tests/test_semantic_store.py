"""Test semantic memory functionality"""
import pytest
import tempfile
import os


def test_ingest_text():
    """Test ingesting text into semantic memory"""
    from synapse.rag.semantic_ingest import SemanticIngestor
    from synapse.rag.semantic_store import SemanticStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        semantic_store = SemanticStore(temp_db)
        ingestor = SemanticIngestor(semantic_store)
        
        # Ingest some text
        chunk_ids = ingestor.ingest_text(
            content="Test content for semantic search",
            metadata={"source": "test.txt", "type": "test"}
        )
        
        assert len(chunk_ids) > 0
        
        # Retrieve chunks
        chunks = list(semantic_store.chunks)
        assert len(chunks) > 0
        assert any(chunk.metadata.get("source") == "test.txt" for chunk in chunks)


def test_retrieve_chunks():
    """Test retrieving chunks from semantic memory"""
    from synapse.rag.semantic_store import SemanticStore
    from synapse.rag.semantic_retriever import SemanticRetriever
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        semantic_store = SemanticStore(temp_db)
        retriever = SemanticRetriever(semantic_store)
        
        # Ingest some text first
        ingestor = SemanticIngestor(semantic_store)
        ingestor.ingest_text(
            content="Test content for retrieval",
            metadata={"source": "test.txt", "type": "test"}
        )
        
        # Retrieve chunks
        results = retriever.retrieve(
            query="test",
            trigger="external_info_needed",
            top_k=3
        )
        
        assert len(results) > 0
        assert results[0]["content"] is not None


def test_retrieve_by_source():
    """Test retrieving chunks by source"""
    from synapse.rag.semantic_store import SemanticStore
    from synapse.rag.semantic_retriever import SemanticRetriever
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        semantic_store = SemanticStore(temp_db)
        retriever = SemanticRetriever(semantic_store)
        
        # Ingest from multiple sources
        for source in ["file1.txt", "file2.txt"]:
            ingestor = SemanticIngestor(semantic_store)
            ingestor.ingest_text(
                content=f"Content from {source}",
                metadata={"source": source, "type": "code"}
            )
        
        # Retrieve by source
        results = retriever.retrieve(
            query="test",
            trigger="external_info_needed",
            top_k=10
        )
        
        # Filter by source
        file1_results = [r for r in results if r["metadata"].get("source") == "file1.txt"]
        assert len(file1_results) == 3


def test_chunk_metadata():
    """Test that chunk metadata is properly stored"""
    from synapse.rag.semantic_ingest import SemanticIngestor
    from synapse.rag.semantic_store import SemanticStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        semantic_store = SemanticStore(temp_db)
        ingestor = SemanticIngestor(semantic_store)
        
        # Ingest with rich metadata
        chunk_ids = ingestor.ingest_text(
            content="Test content",
            metadata={
                "source": "test.py",
                "type": "code",
                "line_number": 42,
                "function": "test_function",
                "created_at": "2025-01-04T10:00:00Z",
                "author": "test_user"
            }
        )
        
        # Retrieve and verify metadata
        chunks = list(semantic_store.chunks)
        test_chunk = [c for c in chunks if c.metadata.get("source") == "test.py"][0]
        
        assert test_chunk is not None
        assert test_chunk.metadata.get("line_number") == 42
        assert test_chunk.metadata.get("function") == "test_function"
        assert test_chunk.metadata.get("author") == "test_user"
