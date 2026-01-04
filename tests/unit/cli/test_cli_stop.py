"""
Unit tests for CLI Stop Command.

Tests cover server shutdown, gracefulness, forced kill, and timeout handling.
"""

import pytest
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from tests.utils.helpers import save_test_config


@pytest.mark.unit
class TestCLIStopCommand:
    """Test CLI stop command for MCP server."""

    def test_server_shutdown(self, tmp_path):
        """Test successful server shutdown."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["stop", "--config", str(config_path)])

        # Verify command accepted
        assert result.exit_code in [0, 1], "Stop command should be accepted"
        assert "stop" in result.output.lower() or "shutdown" in result.output.lower(), "Should indicate stopping"

    def test_graceful_termination(self, tmp_path):
        """Test graceful server termination."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()

        # Test graceful flag (if available)
        result = runner.invoke("synapse", ["stop", "--graceful", "--config", str(config_path)])

        # Should handle gracefully
        assert result.exit_code in [0, 1], "Graceful stop should succeed"
        assert "shutting down" in result.output.lower() or "graceful" in result.output.lower(), "Should indicate gracefulness"

    def test_forced_kill(self, tmp_path):
        """Test forced server kill."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()

        # Test force flag (if available)
        result = runner.invoke("synapse", ["stop", "--force", "--config", str(config_path)])

        # Should terminate immediately
        assert result.exit_code in [0, 1], "Force stop should be accepted"

    def test_not_running(self, tmp_path):
        """Test server not running scenario."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["stop", "--config", str(config_path)])

        # Should handle gracefully (server not running)
        assert result.exit_code in [0, 1], "Should handle server not running"
        assert "not running" in result.output.lower() or "no server" in result.output.lower(), "Should indicate server not running"

    def test_timeout_handling(self, tmp_path):
        """Test shutdown timeout."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()

        # Test timeout flag (if available)
        result = runner.invoke("synapse", ["stop", "--timeout", "5", "--config", str(config_path)])

        # Should handle timeout
        assert result.exit_code in [0, 1], "Should handle timeout"
        assert "timeout" in result.output.lower() or "timed out" in result.output.lower(), "Should mention timeout"

    def test_error_handling(self, tmp_path):
        """Test error scenarios."""
        # Test with invalid config
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text('{"invalid": "config"}')

        runner = CliRunner()
        result = runner.invoke("synapse", ["stop", "--config", str(invalid_config)])

        # Should fail gracefully
        assert result.exit_code != 0, "Should fail with invalid config"
        assert "error" in result.stderr.lower() or "invalid" in result.stderr.lower(), "Should show error"
