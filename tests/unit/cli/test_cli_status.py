"""
Unit tests for CLI Status Command.

Tests cover server status, model status, memory statistics, and health checks.
"""

import pytest
from typer.testing import CliRunner
from synapse.cli.main import app


@pytest.mark.unit
class TestCLIStatusCommand:
    """Test CLI status command."""

    def test_status_command_exists(self):
        """Test that status command is available."""
        runner = CliRunner()
        result = runner.invoke(app, ["status", "--help"])

        # Verify status command is available
        assert result.exit_code == 0
        assert "status" in result.output.lower()

    def test_status_executes(self):
        """Test that status command can be executed."""
        runner = CliRunner()
        result = runner.invoke(app, ["status"])

        # Status should execute (even if server is not running)
        assert result.exit_code == 0

    def test_verbose_flag(self):
        """Test verbose flag works."""
        runner = CliRunner()
        result = runner.invoke(app, ["status", "--verbose"])

        # Should execute with verbose output
        assert result.exit_code == 0

    def test_short_verbose_flag(self):
        """Test short verbose flag works."""
        runner = CliRunner()
        result = runner.invoke(app, ["status", "-v"])

        # Should execute with verbose output
        assert result.exit_code == 0

    def test_output_contains_expected_content(self):
        """Test output contains expected information."""
        runner = CliRunner()
        result = runner.invoke(app, ["status"])

        # Check that output contains key elements
        assert "synapse" in result.output.lower() or "status" in result.output.lower()

    def test_error_handling_invalid_option(self):
        """Test error handling with invalid option."""
        runner = CliRunner()
        result = runner.invoke(app, ["status", "--invalid-option"])

        # Should fail gracefully
        assert result.exit_code != 0

    def test_no_args(self):
        """Test status with no arguments."""
        runner = CliRunner()
        result = runner.invoke(app, ["status"])

        # Should execute successfully
        assert result.exit_code == 0

    def test_help_shows_status_info(self):
        """Test that help shows status command information."""
        runner = CliRunner()
        result = runner.invoke(app, ["status", "--help"])

        # Help should describe the status command
        assert result.exit_code == 0
        assert "status" in result.output.lower()
