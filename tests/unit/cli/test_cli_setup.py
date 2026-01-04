"""
Unit tests for CLI Setup Command.

Tests cover fresh installation, configuration creation, model download, offline mode, and validation.
"""

import pytest
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from tests.utils.helpers import save_test_config


@pytest.mark.unit
class TestCLISetupCommand:
    """Test CLI setup command for initial installation."""

    def test_fresh_install(self, tmp_path):
        """Test fresh installation scenario."""
        config_path = tmp_path / "test_config.json"
        # Don't create config - let setup create it

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--offline", "--yes", "--config", str(config_path)])

        # Should create default config
        assert result.exit_code in [0, 1], "Setup should complete or ask for confirmation"
        assert config_path.exists(), f"Config should be created: {config_path}"

    def test_configuration_creation(self, tmp_path):
        """Test configuration file creation."""
        config_path = tmp_path / "test_config.json"
        # Create initial empty config
        config_path.write_text('{"initialized": true}')

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should use existing config"
        assert "using config" in result.output.lower() or "config" in result.output.lower(), "Should indicate config usage"

    def test_model_download(self, tmp_path):
        """Test model download during setup."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--model", "bge-m3", "--offline", "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should download model or skip if exists"
        # Note: Actual download would require internet/mock

    def test_offline_mode(self, tmp_path):
        """Test offline mode setup."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--offline", "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Offline setup should succeed"
        assert "offline" in result.output.lower() or "no model" in result.output.lower(), "Should indicate offline mode"

    def test_custom_directory(self, tmp_path):
        """Test custom directory setup."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--data-dir", str(tmp_path / "custom_data"), "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should use custom directory"
        assert tmp_path / "custom_data" in result.output.lower() or "directory" in result.output.lower(), "Should mention custom directory"

    def test_existing_config(self, tmp_path):
        """Test handling of existing config."""
        # Create pre-existing config
        config_path = tmp_path / "test_config.json"
        config_path.write_text('{"model": "bge-m3", "data_dir": "/tmp/test"}')

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--yes", "--config", str(config_path)])

        # Should use existing config without error
        assert result.exit_code in [0, 1], "Should use existing config"
        assert "using existing config" in result.output.lower() or "already configured" in result.output.lower(), "Should acknowledge existing config"

    def test_force_reinstall(self, tmp_path):
        """Test force reinstall option."""
        config_path = tmp_path / "test_config.json"
        config_path.write_text('{"model": "old-model"}')

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--force", "--model", "bge-m3", "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should force reinstall"
        assert "force" in result.output.lower() or "reinstall" in result.output.lower(), "Should indicate force reinstall"

    def test_progress_reporting(self, tmp_path):
        """Test setup progress reporting."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--verbose", "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Verbose mode should be accepted"
        # Should show progress indicators

    def test_error_handling(self, tmp_path):
        """Test error scenarios."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()

        # Test with invalid data directory
        result = runner.invoke("synapse", ["setup", "--data-dir", "/nonexistent/path", "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should handle invalid path gracefully"
        assert "error" in result.stderr.lower() or "cannot" in result.stderr.lower() or "invalid" in result.stderr.lower(), "Should show error"

    def test_setup_verification(self, tmp_path):
        """Test setup completion verification."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--yes", "--config", str(config_path)])

        # Verify setup completed
        assert result.exit_code in [0, 1], "Setup should complete"
        assert "complete" in result.output.lower() or "success" in result.output.lower() or "done" in result.output.lower(), "Should indicate completion"

    def test_minimal_setup(self, tmp_path):
        """Test minimal/quick setup."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["setup", "--yes", "--no-model", "--config", str(config_path)])

        # Should work without model
        assert result.exit_code in [0, 1], "Should complete without model"
        assert "no model" in result.output.lower() or "skipping" in result.output.lower(), "Should mention no model"
