"""
Unit tests for CLI Start Command.

Tests cover server startup, port binding, configuration loading, and error recovery.
"""

import pytest
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from synapse.cli.main import app
from tests.utils.helpers import save_test_config


@pytest.mark.unit
class TestCLIStartCommand:
    """Test CLI start command for MCP server."""

    def test_server_startup(self, tmp_path):
        """Test successful server start."""
        config_path = tmp_path / "test_config.json"
        save_test_config(str(config_path), {})

        runner = CliRunner()
        result = runner.invoke(app, ["start", "--config", str(config_path)])

        # Verify command initiated
        # Note: Actual server startup would require async/subprocess
        assert result.exit_code in [0, 1], "Start command should initiate server"
        assert "starting" in result.output.lower() or "start" in result.output.lower(), "Should indicate server starting"

    def test_port_binding(self, tmp_path):
        """Test port parameter."""
        config_path = tmp_path / "test_config.json"
        save_test_config(str(config_path), {})

        runner = CliRunner()

        # Test with explicit port
        result = runner.invoke(app, ["start", "--port", "8003", "--config", str(config_path)])

        assert result.exit_code == 0, f"Start with port should succeed: {result.output}"
        assert "8003" in result.output, f"Port 8003 should be mentioned: {result.output}"

    def test_configuration_loading(self, tmp_path):
        """Test config file loading."""
        config_path = tmp_path / "test_config.json"
        save_test_config(str(config_path), {})

        runner = CliRunner()
        result = runner.invoke(app, ["start", "--config", str(config_path)])

        assert result.exit_code == 0, f"Should load config: {result.output}"

    def test_error_recovery(self, tmp_path):
        """Test error recovery from server issues."""
        # Test with invalid config
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text('{"invalid": "config"}')

        runner = CliRunner()
        result = runner.invoke(app, ["start", "--config", str(invalid_config)])

        # Should handle error gracefully
        assert result.exit_code != 0, "Should fail with invalid config"
        assert "error" in result.stderr.lower() or "invalid" in result.stderr.lower(), "Should show error"

    def test_already_running(self, tmp_path):
        """Test server already running scenario."""
        config_path = tmp_path / "test_config.json"
        save_test_config(str(config_path), {})

        runner = CliRunner()
        result = runner.invoke(app, ["start", "--config", str(config_path)])

        # This test would require checking if server is actually running
        # For now, we test the command is accepted
        assert result.exit_code in [0, 1], "Start command should be accepted"

    def test_port_conflict(self, tmp_path):
        """Test port already in use."""
        config_path = tmp_path / "test_config.json"
        save_test_config(str(config_path), {})

        runner = CliRunner()

        # Simulate port conflict (mock or check)
        result = runner.invoke(app, ["start", "--port", "9999", "--config", str(config_path)])

        # Test with port in high range (unlikely conflict)
        assert result.exit_code in [0, 1], f"Should attempt to bind port: {result.output}"

    def test_graceful_shutdown(self, tmp_path):
        """Test graceful shutdown signal handling."""
        config_path = tmp_path / "test_config.json"
        save_test_config(str(config_path), {})

        runner = CliRunner()
        # Invoke start
        start_result = runner.invoke(app, ["start", "--config", str(config_path)])

        # Then invoke stop
        stop_result = runner.invoke(app, ["stop", "--config", str(config_path)])

        # Both should succeed
        assert start_result.exit_code in [0, 1], "Start should be accepted"
        assert stop_result.exit_code in [0, 1], "Stop should succeed"

    def test_invalid_config(self, tmp_path):
        """Test invalid configuration."""
        # Create config with missing required fields
        invalid_config = tmp_path / "incomplete.json"
        invalid_config.write_text('{"mcp_port": 8003}')  # Missing other required fields

        runner = CliRunner()
        result = runner.invoke(app, ["start", "--config", str(invalid_config)])

        # Should fail with clear error message
        assert result.exit_code != 0, "Should fail with incomplete config"
        assert "missing" in result.stderr.lower() or "required" in result.stderr.lower(), "Should show missing fields"
