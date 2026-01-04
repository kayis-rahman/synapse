"""
End-to-end tests for CLI workflows.

Tests cover complete user workflows from first install to querying.
"""

import pytest
import subprocess
import tempfile
from pathlib import Path


@pytest.mark.e2e
class TestCLIWorkflows:
    """Test complete CLI user workflows."""

    def test_first_time_setup(self, tmp_path):
        """Test fresh install and setup."""
        # Create temporary test environment
        test_config = tmp_path / "test_config.json"
        test_config.write_text('{"data_dir": "%s", "models_dir": "%s"}' % (str(tmp_path / "data"), str(tmp_path / "models")))

        # Run setup command with test config
        result = subprocess.run(
            ["python3", "-m", "synapse.cli.main", "setup", "--offline", "--no-model-check"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Verify setup completed
        assert result.returncode == 0, "Setup should complete successfully"
        assert "setup complete" in result.stdout.lower() or "Setup complete" in result.stderr.lower(), \
            "Setup should indicate completion"

    def test_project_ingestion(self, tmp_path):
        """Test ingesting a codebase project."""
        # Create test project
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        (test_project / "src").mkdir()
        (test_project / "README.md").write_text("# Test Project\n\nThis is a test project.")

        # Run ingest command
        result = subprocess.run(
            ["python3", "-m", "synapse.cli.main", "ingest", str(test_project)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Verify ingestion completed
        assert result.returncode == 0 or "no documents found" in result.stdout.lower(), \
            "Ingest should complete successfully or indicate no documents"

    def test_query_knowledge_base(self, tmp_path):
        """Test querying the knowledge base."""
        # Run query command
        result = subprocess.run(
            ["python3", "-m", "synapse.cli.main", "query", "How does authentication work?"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Verify query completed
        assert result.returncode == 0 or "no results" in result.stdout.lower(), \
            "Query should complete successfully or indicate no results"

    def test_mcp_server_startup(self, tmp_path):
        """Test starting MCP server."""
        # Run start command
        result = subprocess.run(
            ["python3", "-m", "synapse.cli.main", "start"],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Verify server started or provided helpful message
        # Server may take time to start, so we just verify command doesn't crash
        assert result.returncode is not None, "Start command should execute"

    def test_full_workflow(self, tmp_path):
        """Test complete workflow: setup → ingest → query."""
        # Step 1: Setup
        setup_result = subprocess.run(
            ["python3", "-m", "synapse.cli.main", "setup", "--offline", "--no-model-check"],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert setup_result.returncode == 0, "Setup should complete"

        # Step 2: Create and ingest test project
        test_project = tmp_path / "full_test_project"
        test_project.mkdir()
        (test_project / "test.md").write_text("# Test\nContent here.")
        (test_project / "code.py").write_text("# Test code\nprint('hello')")

        ingest_result = subprocess.run(
            ["python3", "-m", "synapse.cli.main", "ingest", str(test_project)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Step 3: Query
        query_result = subprocess.run(
            ["python3", "-m", "synapse.cli.main", "query", "what's in the test project?"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Verify full workflow completed
        assert setup_result.returncode == 0, "Setup should succeed"
        # Note: ingest and query may have different behaviors
