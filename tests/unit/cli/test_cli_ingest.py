"""
Unit tests for CLI Ingest Command.

Tests cover file ingestion, directory ingestion, progress reporting, error handling, and configuration.
"""

import pytest
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from synapse.cli.main import app
from tests.utils.helpers import (
    save_test_config,
    load_test_config,
    create_test_document,
    assert_between,
)


@pytest.mark.unit
class TestCLIIngestCommand:
    """Test synapse ingest CLI command."""

    def test_ingest_file(self, tmp_path):
        """Test ingesting a single file."""
        # Create test file
        test_file = tmp_path / "test_file.py"
        test_file.write_text("# Test file content\nprint('hello')")

        # Run ingest command
        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_file)])

        # Verify command executed successfully
        assert result.exit_code == 0, f"Ingest should succeed: {result.output}"
        assert "ingested" in result.output.lower() or "ingested" in result.stderr.lower()

    def test_ingest_directory(self, tmp_path):
        """Test ingesting a directory."""
        # Create test directory with files
        test_dir = tmp_path / "test_project"
        test_dir.mkdir()
        (test_dir / "README.md").write_text("# Test Project\nprint('hello')")
        (test_dir / "code.py").write_text("print('hello')")
        (test_dir / "subdir").mkdir()
        (test_dir / "subdir" / "file.py").write_text("# Nested file")

        # Run ingest command
        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_dir)])

        # Verify command executed
        assert result.exit_code == 0, f"Ingest should succeed: {result.output}"
        assert "test_project" in result.output.lower() or "ingested" in result.stderr.lower()

    def test_progress_reporting(self, tmp_path):
        """Test progress reporting during ingestion."""
        # Create test directory with multiple files
        test_dir = tmp_path / "test_project"
        test_dir.mkdir()
        (test_dir / "file1.py").write_text("content 1")
        (test_dir / "file2.py").write_text("content 2")
        (test_dir / "file3.py").write_text("content 3")

        # Run ingest and verify progress shown
        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(test_dir)])

        assert result.exit_code == 0
        assert "processed" in result.output.lower()

    def test_error_handling_invalid_path(self, tmp_path):
        """Test error handling with invalid path."""
        runner = CliRunner()
        result = runner.invoke(app, ["ingest", "/nonexistent/path"])

        # Should fail gracefully
        assert result.exit_code != 0
        assert "error" in result.output.lower() or "error" in result.stderr.lower()

    def test_error_handling_empty_directory(self, tmp_path):
        """Test error handling with empty directory."""
        empty_dir = tmp_path / "empty_dir"
        empty_dir.mkdir()

        runner = CliRunner()
        result = runner.invoke(app, ["ingest", str(empty_dir)])

        # Should handle gracefully (no files to ingest)
        assert result.exit_code == 0
        assert "no documents" in result.output.lower()

    def test_empty_input(self, tmp_path):
        """Test with empty input."""
        runner = CliRunner()

        result = runner.invoke(app, ["ingest"])

        # Should show usage/help for empty input
        assert result.exit_code != 0
        assert "usage" in result.output.lower() or "help" in result.stderr.lower()

    def test_invalid_path(self, tmp_path):
        """Test with invalid path type (if supported)."""
        # Most file systems only support regular files

        runner = CliRunner()
        result = runner.invoke(app, ["ingest", "/dev/invalid"])

        # Should fail or show error
        assert result.exit_code != 0
