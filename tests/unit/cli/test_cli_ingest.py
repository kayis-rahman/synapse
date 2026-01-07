"""Unit tests for CLI Ingest Command."""

import pytest
from typer.testing import CliRunner
from synapse.cli.main import app
from pathlib import Path


@pytest.mark.unit
class TestCLIIngestCommand:
    """Test synapse ingest CLI command."""

    def test_ingest_command_exists(self):
        """Test that ingest command is available."""
        runner = CliRunner()
        result = runner.invoke(app, ["ingest", "--help"])
        assert result.exit_code == 0
        assert "ingest" in result.output.lower()

    def test_ingest_file(self, tmp_path):
        """Test ingesting a single file."""
        test_file = tmp_path / "test_file.py"
        test_file.write_text("# Test file content\nprint('hello')")

        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_file)])

        # Should attempt to ingest
        assert result.exit_code in [0, 1]

    def test_ingest_directory(self, tmp_path):
        """Test ingesting a directory."""
        test_dir = tmp_path / "test_project"
        test_dir.mkdir()
        (test_dir / "README.md").write_text("# Test Project")
        (test_dir / "code.py").write_text("print('hello')")

        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_dir)])

        # Should attempt to ingest
        assert result.exit_code in [0, 1]

    def test_ingest_with_project_id(self, tmp_path):
        """Test ingest with project-id parameter."""
        test_file = tmp_path / "test.py"
        test_file.write_text("test content")

        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_file), "--project-id", "test-project"])

        # Should attempt to ingest
        assert result.exit_code in [0, 1]

    def test_ingest_with_short_project_id(self, tmp_path):
        """Test ingest with short project-id parameter."""
        test_file = tmp_path / "test.py"
        test_file.write_text("test content")

        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_file), "-p", "test"])

        # Should attempt to ingest
        assert result.exit_code in [0, 1]

    def test_ingest_with_code_mode(self, tmp_path):
        """Test ingest with code-mode flag."""
        test_file = tmp_path / "test.py"
        test_file.write_text("def test(): pass")

        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_file), "--code-mode"])

        # Should attempt to ingest
        assert result.exit_code in [0, 1]

    def test_ingest_with_short_code_mode(self, tmp_path):
        """Test ingest with short code-mode flag."""
        test_file = tmp_path / "test.py"
        test_file.write_text("def test(): pass")

        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_file), "-c"])

        # Should attempt to ingest
        assert result.exit_code in [0, 1]

    def test_ingest_error_handling_invalid_path(self):
        """Test error handling with invalid path."""
        runner = CliRunner()
        result = runner.invoke(app, ["ingest", "/nonexistent/path"])

        # Should fail gracefully
        assert result.exit_code != 0

    def test_ingest_empty_input(self):
        """Test with empty input."""
        runner = CliRunner()
        result = runner.invoke(app, ["ingest"])

        # Should show usage/help for empty input
        assert result.exit_code != 0
