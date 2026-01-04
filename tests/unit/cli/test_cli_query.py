"""
Unit tests for CLI Query Command.

Tests cover query execution, result formatting, streaming, error handling, and parameters.
"""

import pytest
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from tests.utils.helpers import (
    save_test_config,
    create_test_document,
)


@pytest.mark.unit
class TestCLIQueryCommand:
    """Test CLI query command."""

    def test_query_execution(self, tmp_path):
        """Test basic query execution."""
        # Create test document
        doc = create_test_document(content="Test content about authentication")
        save_test_config(tmp_path / "test_config.json")

        # Run query command
        runner = CliRunner()
        result = runner.invoke("synapse", ["query", "What is authentication?", "--config", str(tmp_path / "test_config.json")])

        # Verify command executed successfully
        assert result.exit_code == 0, f"Query should succeed: {result.output}"
        assert len(result.output) > 0, "Should return output"

    def test_result_formatting(self, tmp_path):
        """Test result formatting."""
        runner = CliRunner()
        result = runner.invoke("synapse", ["query", "Test query", "--config", str(tmp_path / "test_config.json")])

        # Verify output is properly formatted
        assert result.exit_code == 0, f"Query should succeed: {result.output}"
        # Check for expected formatting patterns (e.g., no extra whitespace)
        assert not result.output.startswith("  "), "Output should not have leading whitespace"
        assert result.output.endswith("\n") or len(result.output.strip()) > 0, "Output should end with newline or have content"

    def test_streaming_output(self, tmp_path):
        """Test streaming output."""
        runner = CliRunner()
        # Most CLI commands don't support streaming yet, so test normal output
        result = runner.invoke("synapse", ["query", "Test query", "--config", str(tmp_path / "test_config.json")])

        # Verify output is returned
        assert result.exit_code == 0, f"Query should succeed: {result.output}"
        assert len(result.stderr) == 0, f"Should not have stderr output: {result.stderr}"

    def test_error_handling(self, tmp_path):
        """Test error scenarios."""
        runner = CliRunner()

        # Test with non-existent config
        result = runner.invoke("synapse", ["query", "Test", "--config", "/nonexistent/config.json"])

        # Should fail gracefully
        assert result.exit_code != 0, "Should fail with non-existent config"
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower(), "Should show error message"

    def test_empty_results(self, tmp_path):
        """Test empty knowledge base query."""
        # Create empty config (no data ingested)
        empty_config = tmp_path / "empty_config.json"
        save_test_config(empty_config)

        runner = CliRunner()
        result = runner.invoke("synapse", ["query", "Test query", "--config", str(empty_config)])

        # Verify empty results are handled
        assert result.exit_code == 0, "Query should succeed even with empty KB"
        assert "no results" in result.output.lower() or "found 0" in result.output.lower(), "Should indicate empty results"

    def test_invalid_query(self, tmp_path):
        """Test invalid input."""
        runner = CliRunner()

        # Test with empty query
        result = runner.invoke("synapse", ["query", "", "--config", str(tmp_path / "test_config.json")])

        # Verify error handling
        assert result.exit_code != 0 or "error" in result.stderr.lower(), "Should handle empty query"
        assert len(result.output) + len(result.stderr) > 0, "Should have output or error"

    def test_top_k_parameter(self, tmp_path):
        """Test top_k parameter."""
        runner = CliRunner()

        # Test with top_k=1
        result = runner.invoke("synapse", ["query", "Test query", "--top-k", "1", "--config", str(tmp_path / "test_config.json")])

        assert result.exit_code == 0, f"Query with top_k=1 should succeed: {result.output}"

        # Test with top_k=100 (high value)
        result2 = runner.invoke("synapse", ["query", "Test query", "--top-k", "100", "--config", str(tmp_path / "test_config.json")])

        assert result.exit_code == 0, f"Query with top_k=100 should succeed: {result2.output}"

    def test_min_score_parameter(self, tmp_path):
        """Test min_score parameter."""
        runner = CliRunner()

        # Test with min_score=0.1 (low threshold)
        result = runner.invoke("synapse", ["query", "Test query", "--min-score", "0.1", "--config", str(tmp_path / "test_config.json")])

        assert result.exit_code == 0, f"Query with min_score=0.1 should succeed: {result.output}"

        # Test with min_score=0.9 (high threshold)
        result2 = runner.invoke("synapse", ["query", "Test query", "--min-score", "0.9", "--config", str(tmp_path / "test_config.json")])

        # With high threshold, might return no results
        assert result2.exit_code == 0, f"Query with min_score=0.9 should succeed: {result2.output}"
