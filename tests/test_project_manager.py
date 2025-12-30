"""Test ProjectManager functionality."""
import os
import tempfile
import pytest
from mcp_server.project_manager import ProjectManager, generate_short_uuid

def test_generate_short_uuid():
    """Test short UUID generation."""
    uuid_str = generate_short_uuid()
    assert len(uuid_str) == 8
    assert isinstance(uuid_str, str)

def test_create_project():
    """Test project creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = ProjectManager(base_data_dir=tmpdir)

        project = pm.create_project("testproject")

        assert "testproject" in project["project_id"]
        assert project["status"] == "active"
        assert os.path.exists(project["chroma_path"])
        assert project["name"] == "testproject"

def test_list_projects():
    """Test project listing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = ProjectManager(base_data_dir=tmpdir)

        pm.create_project("project1")
        pm.create_project("project2")

        projects = pm.list_projects()
        assert len(projects) == 2

def test_delete_project():
    """Test project deletion."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = ProjectManager(base_data_dir=tmpdir)

        project = pm.create_project("testproject")
        project_id = project["project_id"]

        success = pm.delete_project(project_id)
        assert success == True

        # Verify deletion
        assert pm.get_project(project_id) is None

def test_validate_project_name():
    """Test project name validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = ProjectManager(base_data_dir=tmpdir)

        # Valid name
        pm._validate_project_name("valid-name")

        # Invalid characters
        with pytest.raises(ValueError):
            pm._validate_project_name("invalid/name")

        # Too long
        with pytest.raises(ValueError):
            pm._validate_project_name("a" * 101)

        # Empty
        with pytest.raises(ValueError):
            pm._validate_project_name("")

def test_get_project_info():
    """Test getting project information."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = ProjectManager(base_data_dir=tmpdir)

        project = pm.create_project("testproject")
        project_id = project["project_id"]

        # Get project
        retrieved = pm.get_project(project_id)
        assert retrieved is not None
        assert retrieved["project_id"] == project_id
        assert retrieved["name"] == "testproject"

def test_validate_project_id():
    """Test project ID validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = ProjectManager(base_data_dir=tmpdir)

        project = pm.create_project("testproject")
        project_id = project["project_id"]

        # Valid ID
        assert pm.validate_project_id(project_id) == True

        # Invalid ID
        assert pm.validate_project_id("nonexistent-abc12345") == False
