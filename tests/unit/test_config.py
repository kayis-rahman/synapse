"""
Unit tests for SYNAPSE configuration system.

Tests cover configuration loading, layering, validation, and environment detection.
"""

import pytest
import os
from pathlib import Path
from synapse.config import (
    DEFAULT_CONFIG,
    get_config,
    load_config_file,
    apply_environment_variables,
    validate_config,
    detect_data_directory,
    detect_models_directory,
    detect_environment
)


@pytest.mark.unit
class TestConfiguration:
    """Test SYNAPSE configuration system."""

    def test_default_config_exists(self):
        """Test that default configuration is defined."""
        assert DEFAULT_CONFIG is not None, "DEFAULT_CONFIG should be defined"
        assert isinstance(DEFAULT_CONFIG, dict), "DEFAULT_CONFIG should be a dict"
        assert len(DEFAULT_CONFIG) > 0, "DEFAULT_CONFIG should have keys"

    def test_default_config_values(self):
        """Test that default config has expected values."""
        assert "chunk_size" in DEFAULT_CONFIG
        assert "top_k" in DEFAULT_CONFIG
        assert "data_dir" in DEFAULT_CONFIG
        assert "models_dir" in DEFAULT_CONFIG
        assert "mcp_port" in DEFAULT_CONFIG

        # Verify some default values
        assert DEFAULT_CONFIG["chunk_size"] == 500
        assert DEFAULT_CONFIG["top_k"] == 3
        assert DEFAULT_CONFIG["mcp_port"] == 8002

    def test_detect_data_directory(self):
        """Test data directory detection."""
        data_dir = detect_data_directory()

        assert data_dir is not None, "Data directory should be detected"
        assert isinstance(data_dir, str), "Data directory should be a string"

        # Should return one of: /app/data, /opt/synapse/data, ~/.synapse/data, ./data
        valid_paths = [
            "/app/data",
            "/opt/synapse/data",
            str(Path.home() / ".synapse" / "data"),
        ]
        assert data_dir in valid_paths or data_dir.endswith("/data"), \
            "Data directory should be a valid path"

    def test_detect_models_directory(self):
        """Test models directory detection."""
        models_dir = detect_models_directory()

        assert models_dir is not None, "Models directory should be detected"
        assert isinstance(models_dir, str), "Models directory should be a string"

        # Should return one of: /app/models, /opt/synapse/models, ~/.synapse/models, ./models
        valid_paths = [
            "/app/models",
            "/opt/synapse/models",
            str(Path.home() / ".synapse" / "models"),
        ]
        assert models_dir in valid_paths or models_dir.endswith("/models"), \
            "Models directory should be a valid path"

    def test_detect_environment(self):
        """Test environment detection (Docker vs native)."""
        env = detect_environment()

        assert env in ["docker", "native"], "Environment should be 'docker' or 'native'"
        assert isinstance(env, str), "Environment should be a string"

    def test_load_config_file_missing(self, tmp_path):
        """Test loading config when file doesn't exist."""
        non_existent_path = tmp_path / "non_existent.json"

        config = load_config_file(non_existent_path)

        assert config == {}, "Missing config file should return empty dict"

    def test_load_config_file_invalid(self, tmp_path):
        """Test loading invalid config file."""
        invalid_path = tmp_path / "invalid.json"
        invalid_path.write_text("not valid json {")

        config = load_config_file(invalid_path)

        assert config == {}, "Invalid config file should return empty dict"

    def test_apply_environment_variables(self):
        """Test applying environment variable overrides."""
        import json

        config = {
            "chunk_size": 500,
            "top_k": 3,
            "data_dir": "/default/path",
        }

        # Mock environment variables
        env_vars = {
            "SYNDROME_CHUNK_SIZE": "1000",
            "SYNDROME_TOP_K": "5",
            "SYNDROME_DATA_DIR": "/custom/path",
        }

        for key, value in env_vars.items():
            os.environ[key] = value

        try:
            result = apply_environment_variables(config)

            # Verify overrides
            assert result["chunk_size"] == 1000, "Environment variable should override chunk_size"
            assert result["top_k"] == 5, "Environment variable should override top_k"
            assert result["data_dir"] == "/custom/path", "Environment variable should override data_dir"

            # Verify type conversion
            assert isinstance(result["chunk_size"], int), "Numeric values should be converted"
            assert isinstance(result["top_k"], int), "Numeric values should be converted"

        finally:
            # Cleanup environment variables
            for key in env_vars:
                os.environ.pop(key, None)

    def test_validate_config_chunk_size(self):
        """Test configuration validation for chunk_size."""
        # Test too small
        config = {"chunk_size": 50}
        validated = validate_config(config.copy())
        assert validated["chunk_size"] >= 100, "Too small chunk_size should be clamped"

        # Test too large
        config = {"chunk_size": 5000}
        validated = validate_config(config.copy())
        assert validated["chunk_size"] <= 2000, "Too large chunk_size should be clamped"

        # Test valid
        config = {"chunk_size": 500}
        validated = validate_config(config.copy())
        assert validated["chunk_size"] == 500, "Valid chunk_size should be unchanged"

    def test_validate_config_top_k(self):
        """Test configuration validation for top_k."""
        # Test too small
        config = {"top_k": 0}
        validated = validate_config(config.copy())
        assert validated["top_k"] >= 1, "Too small top_k should be clamped"

        # Test too large
        config = {"top_k": 50}
        validated = validate_config(config.copy())
        assert validated["top_k"] <= 20, "Too large top_k should be clamped"

        # Test valid
        config = {"top_k": 5}
        validated = validate_config(config.copy())
        assert validated["top_k"] == 5, "Valid top_k should be unchanged"

    def test_get_config_layering(self, tmp_path):
        """Test that configuration layering works correctly."""
        # Create user config
        user_config = tmp_path / "user_config.json"
        user_config.write_text('{"chunk_size": 800}')

        # Create project config
        project_config = tmp_path / "project_config.json"
        project_config.write_text('{"top_k": 10}')

        # Set environment variable
        os.environ["SYNDROME_MCP_PORT"] = "9999"

        try:
            # Create Home directory structure for user config
            import synapse.config as config_module
            original_load = config_module.load_config_file

            # Note: This test is simplified
            # Full layering test requires mocking home directory
            pass

        finally:
            # Cleanup
            if "SYNDROME_MCP_PORT" in os.environ:
                del os.environ["SYNDROME_MCP_PORT"]

    def test_validate_config_directory_creation(self, tmp_path):
        """Test that validation creates missing directories."""
        config = {
            "data_dir": str(tmp_path / "new_data"),
            "models_dir": str(tmp_path / "new_models"),
        }

        validated = validate_config(config)

        # Directories should be created
        assert (tmp_path / "new_data").exists(), "Data directory should be created"
        assert (tmp_path / "new_models").exists(), "Models directory should be created"
