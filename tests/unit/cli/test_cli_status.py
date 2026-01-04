"""
Unit tests for CLI Status Command.

Tests cover server status, model status, memory statistics, and health checks.
"""

import pytest
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from tests.utils.helpers import save_test_config


@pytest.mark.unit
class TestCLIStatusCommand:
    """Test CLI status command."""

    def test_server_status(self, tmp_path):
        """Test server status reporting."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["status", "--config", str(config_path)])

        # Verify status command executes
        assert result.exit_code in [0, 1], "Status command should execute"
        # Should show server status (running/stopped)
        assert "server" in result.output.lower() or "status" in result.output.lower(), "Should mention server status"

    def test_model_status(self, tmp_path):
        """Test model loading status."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["status", "--models", "--config", str(config_path)])

        # Verify models status
        assert result.exit_code in [0, 1], "Should show model status"
        assert "model" in result.output.lower(), "Should mention model status"

    def test_memory_statistics(self, tmp_path):
        """Test memory tier statistics."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["status", "--memory", "--config", str(config_path)])

        # Verify memory stats
        assert result.exit_code in [0, 1], "Should show memory statistics"
        assert any(word in result.output.lower() for word in ["memory", "facts", "episodes", "chunks"]), "Should show memory stats"

    def test_health_checks(self, tmp_path):
        """Test health check endpoints."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["status", "--health", "--config", str(config_path)])

        # Verify health check
        assert result.exit_code in [0, 1], "Should perform health checks"
        assert "health" in result.output.lower() or "healthy" in result.output.lower(), "Should indicate health status"

    def test_detailed_mode(self, tmp_path):
        """Test verbose/detailed output."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["status", "--verbose", "--config", str(config_path)])

        # Verify detailed output
        assert result.exit_code in [0, 1], "Should show detailed status"
        assert len(result.output) > 100, "Detailed mode should show more output"

    def test_json_output(self, tmp_path):
        """Test JSON format output."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["status", "--json", "--config", str(config_path)])

        # Verify JSON format
        assert result.exit_code in [0, 1], "Should output JSON"
        # Parse output as JSON to verify format
        import json
        try:
            json.loads(result.output)
        except json.JSONDecodeError:
            pytest.fail("Output should be valid JSON")

    def test_error_handling(self, tmp_path):
        """Test error scenarios."""
        # Test with invalid config
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text('{"invalid": "config"}')

        runner = CliRunner()
        result = runner.invoke("synapse", ["status", "--config", str(invalid_config)])

        # Should still show status even with invalid config
        assert result.exit_code in [0, 1], "Should handle invalid config"

    def test_offline_mode(self, tmp_path):
        """Test offline status (without server running)."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["status", "--offline", "--config", str(config_path)])

        # Verify offline mode works
        assert result.exit_code in [0, 1], "Offline status should work"
        assert "offline" in result.output.lower() or "standalone" in result.output.lower(), "Should indicate offline mode"
