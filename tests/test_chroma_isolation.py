"""Test ChromaDB isolation."""
import pytest
from mcp_server.chroma_manager import ProjectChromaManager

def test_separate_clients():
    """Test that each project gets separate ChromaDB client."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        chroma_mgr = ProjectChromaManager(tmpdir)

        client1 = chroma_mgr.get_chroma_client("project1-abc12345")
        client2 = chroma_mgr.get_chroma_client("project2-def67890")

        assert client1 != client2

def test_separate_collections():
    """Test that each project gets separate collection."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        chroma_mgr = ProjectChromaManager(tmpdir)

        coll1 = chroma_mgr.get_collection("project1-abc12345", "test")
        coll2 = chroma_mgr.get_collection("project2-def67890", "test")

        coll1.add(documents=["doc1"], embeddings=[[0.1]], ids=["id1"])

        assert coll1.count() == 1
        assert coll2.count() == 0

def test_remove_client():
    """Test removing client from cache."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        chroma_mgr = ProjectChromaManager(tmpdir)

        chroma_mgr.get_chroma_client("project1-abc12345")
        assert "project1-abc12345" in chroma_mgr._clients

        chroma_mgr.remove_client("project1-abc12345")
        assert "project1-abc12345" not in chroma_mgr._clients
