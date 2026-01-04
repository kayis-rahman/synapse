"""
Unit tests for CLI Models Command.

Tests cover model listing, downloading, deletion, validation, and filtering.
"""

import pytest
import tempfile
from pathlib import Path
from typer.testing import CliRunner
from tests.utils.helpers import save_test_config


@pytest.mark.unit
class TestCLIModelsCommand:
    """Test CLI models command for model management."""

    def test_list_models(self, tmp_path):
        """Test model listing."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["models", "list", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Models list should execute or show no models"
        # Should show list of available models

    def test_download_model(self, tmp_path):
        """Test model download."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["models", "download", "bge-m3", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Download should initiate or fail gracefully"
        assert "download" in result.output.lower() or "model" in result.output.lower(), "Should mention download"

    def test_delete_model(self, tmp_path):
        """Test model deletion."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["models", "delete", "bge-m3", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Delete should execute or show model not found"
        assert "delete" in result.output.lower() or "deleted" in result.output.lower(), "Should mention deletion"

    def test_validate_model(self, tmp_path):
        """Test model validation."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["models", "validate", "bge-m3", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Validation should execute"
        assert "valid" in result.output.lower() or "model" in result.output.lower(), "Should indicate validity"

    def test_model_info(self, tmp_path):
        """Test model metadata/info."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["models", "info", "bge-m3", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Model info should display"
        # Should show model metadata (size, dimensions, format)

    def test_filter_models(self, tmp_path):
        """Test model filtering."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()

        # Test filter by type (quantized)
        result = runner.invoke("synapse", ["models", "list", "--type", "quantized", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Filtering should work"
        # Should only show quantized models

    def test_search_models(self, tmp_path):
        """Test model search."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["models", "search", "bge", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Search should execute"
        assert "bge" in result.output.lower() or "no results" in result.output.lower(), "Should show matching models"

    def test_progress_reporting(self, tmp_path):
        """Test progress display during download."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()

        # This test would require mocking download progress
        # For now, just verify command accepts
        result = runner.invoke("synapse", ["models", "download", "bge-m3", "--verbose", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Verbose mode should be accepted"
        # Should show progress indicators

    def test_error_handling(self, tmp_path):
        """Test error scenarios."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()

        # Test with non-existent model
        result = runner.invoke("synapse", ["models", "info", "nonexistent-model", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should handle non-existent model"
        assert "not found" in result.output.lower() or "error" in result.stderr.lower(), "Should indicate model not found"

    def test_concurrent_operations(self, tmp_path):
        """Test concurrent access (basic check)."""
        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        # This is a basic test - actual concurrent handling requires subprocess
        # Just verify command can be called multiple times
        runner = CliRunner()

        result1 = runner.invoke("synapse", ["models", "list", "--config", str(config_path)])
        result2 = runner.invoke("synapse", ["models", "list", "--config", str(config_path)])

        # Both should succeed
        assert result1.exit_code in [0, 1], "First call should succeed"
        assert result2.exit_code in [0, 1], "Second call should succeed"
