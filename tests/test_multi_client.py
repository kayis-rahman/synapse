"""Test multi-client isolation."""
import asyncio
import pytest
import os
import tempfile
from mcp_server.project_manager import ProjectManager
from mcp_server.rag_server import RAGMemoryBackend

@pytest.mark.asyncio
async def test_project_isolation():
    """Test that projects are isolated."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Set env var for test
        os.environ["RAG_DATA_DIR"] = tmpdir

        backend = RAGMemoryBackend()

        project1 = await backend.create_project("testproject1")
        project2 = await backend.create_project("testproject2")

        await backend.add_fact(project1['project']['project_id'], "key1", "value1")
        await backend.add_fact(project2['project']['project_id'], "key2", "value2")

        context1 = await backend.get_context(project1['project']['project_id'])
        context2 = await backend.get_context(project2['project']['project_id'])

        assert len(context1['symbolic']) == 1
        assert len(context2['symbolic']) == 1
        assert context1['symbolic'][0]['key'] == "key1"
        assert context2['symbolic'][0]['key'] == "key2"

@pytest.mark.asyncio
async def test_project_lifecycle():
    """Test full project lifecycle."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["RAG_DATA_DIR"] = tmpdir

        backend = RAGMemoryBackend()

        # Create
        project = await backend.create_project("lifecycle_test")
        project_id = project['project']['project_id']

        # Verify
        info = await backend.get_project_info(project_id)
        assert info['status'] == "success"

        # Add data
        await backend.add_fact(project_id, "test_key", "test_value")

        # List
        projects = await backend.list_projects()
        assert any(p['project_id'] == project_id for p in projects['projects'])

        # Delete
        result = await backend.delete_project(project_id)
        assert result['deleted'] == True

        # Verify deletion
        info_after = await backend.get_project_info(project_id)
        assert info_after['status'] == "not_found"
