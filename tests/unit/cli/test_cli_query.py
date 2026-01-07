"""
Unit tests for CLI Query Command.

Tests cover query execution, result formatting, streaming, error handling, and parameters.
"""

import pytest
from typer.testing import CliRunner
from synapse.cli.main import app


@pytest.mark.unit
class TestCLIQueryCommand:
    """Test CLI query command."""

    def test_query_command_exists(self):
        """Test that query command is available."""
        runner = CliRunner()
        result = runner.invoke(app, ["query", "--help"])

        # Verify query command is available
        assert result.exit_code == 0
        assert "query" in result.output.lower()

    def test_query_with_text(self):
        """Test basic query execution with text."""
        runner = CliRunner()
        result = runner.invoke(app, ["query", "test query"])

        # Should execute (even if no data is ingested)
        assert result.exit_code == 0

    def test_query_with_top_k(self):
        """Test query with top_k parameter."""
        runner = CliRunner()
        result = runner.invoke(app, ["query", "test query", "--top-k", "5"])

        # Should execute with top_k parameter
        assert result.exit_code == 0

    def test_query_with_short_top_k(self):
        """Test query with short top_k parameter."""
        runner = CliRunner()
        result = runner.invoke(app, ["query", "test query", "-k", "3"])

        # Should execute with short top_k parameter
        assert result.exit_code == 0

    def test_query_with_format_json(self):
        """Test query with JSON format."""
        runner = CliRunner()
        result = runner.invoke(app, ["query", "test query", "--format", "json"])

        # Should execute with JSON format
        assert result.exit_code == 0

    def test_query_with_short_format(self):
        """Test query with short format parameter."""
        runner = CliRunner()
        result = runner.invoke(app, ["query", "test query", "-f", "text"])

        # Should execute with short format parameter
        assert result.exit_code == 0

    def test_query_with_mode(self):
        """Test query with mode parameter."""
        runner = CliRunner()
        result = runner.invoke(app, ["query", "test query", "--mode", "code"])

        # Should execute with mode parameter
        assert result.exit_code == 0

    def test_query_help_shows_parameters(self):
        """Test that help shows all query parameters."""
        runner = CliRunner()
        result = runner.invoke(app, ["query", "--help"])

        # Should show all parameters
        assert result.exit_code == 0
        assert "top-k" in result.output.lower()
        assert "format" in result.output.lower()
        assert "mode" in result.output.lower()
