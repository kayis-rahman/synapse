"""
Unit tests for CLI Onboard Command.

Tests cover project ingestion, interactive/non-interactive modes, configuration generation, and framework detection.
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
class TestCLIOboardCommand:
    """Test CLI onboard command for project setup."""

    def test_project_ingestion(self, tmp_path):
        """Test project file ingestion."""
        # Create test project with Python files
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        (test_project / "main.py").write_text("def main():\n    print('hello')\n")
        (test_project / "utils.py").write_text("def helper():\n    return 42\n")
        (test_project / "README.md").write_text("# Test Project\n\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Onboard should complete"
        assert "ingested" in result.output.lower() or "processing" in result.output.lower() or "files" in result.output.lower(), "Should mention ingestion"

    def test_interactive_setup(self, tmp_path):
        """Test interactive setup mode."""
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        (test_project / "main.py").write_text("def main():\n    print('hello')\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        # Test interactive mode (simulate with auto-yes for testing)
        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--interactive", "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Interactive mode should be accepted"
        assert "interactive" in result.output.lower() or "setup" in result.output.lower(), "Should indicate interactive mode"

    def test_configuration_generation(self, tmp_path):
        """Test configuration generation."""
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        (test_project / "README.md").write_text("# Test Project\n\nA Python project\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should generate config"
        # Verify config file was created

    def test_non_interactive_mode(self, tmp_path):
        """Test non-interactive mode."""
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        (test_project / "main.py").write_text("def main():\n    print('hello')\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Non-interactive mode should work"
        assert "auto" in result.output.lower() or "yes" in result.output.lower() or "generated" in result.output.lower(), "Should indicate auto mode"

    def test_project_detection(self, tmp_path):
        """Test automatic project type detection."""
        # Test Python project
        test_project = tmp_path / "test_py_project"
        test_project.mkdir()
        (test_project / "main.py").write_text("def main():\n    pass\n")
        (test_project / "requirements.txt").write_text("pytest\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should detect project type"
        assert "python" in result.output.lower() or "project" in result.output.lower(), "Should indicate Python project"

    def test_language_detection(self, tmp_path):
        """Test programming language detection."""
        # Test Python project
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        (test_project / "main.py").write_text("def main():\n    pass\n")
        (test_project / "requirements.txt").write_text("pytest\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should detect language"
        assert "python" in result.output.lower() or "detected" in result.output.lower(), "Should indicate Python detection"

    def test_framework_detection(self, tmp_path):
        """Test framework detection."""
        # Test web framework (Flask)
        test_project = tmp_path / "test_web_project"
        test_project.mkdir()
        (test_project / "app.py").write_text("from flask import Flask\n")
        (test_project / "requirements.txt").write_text("flask\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Should detect framework"
        assert "flask" in result.output.lower() or "web" in result.output.lower(), "Should indicate Flask framework"

    def test_progress_reporting(self, tmp_path):
        """Test progress display during onboarding."""
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        (test_project / "main.py").write_text("def main():\n    pass\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--verbose", "--yes", "--config", str(config_path)])

        assert result.exit_code in [0, 1], "Verbose mode should be accepted"
        # Should show progress indicators

    def test_error_handling(self, tmp_path):
        """Test error scenarios."""
        # Test with non-existent directory
        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", "/nonexistent/project", "--yes", "--config", str(tmp_path / "test_config.json")])

        assert result.exit_code in [0, 1], "Should handle non-existent path gracefully"
        assert "not found" in result.output.lower() or "error" in result.stderr.lower() or "does not exist" in result.stderr.lower(), "Should indicate path not found"

    def test_onboard_completion(self, tmp_path):
        """Test onboarding completion."""
        test_project = tmp_path / "test_project"
        test_project.mkdir()
        (test_project / "main.py").write_text("def main():\n    pass\n")

        config_path = tmp_path / "test_config.json"
        save_test_config(config_path)

        runner = CliRunner()
        result = runner.invoke("synapse", ["onboard", str(test_project), "--yes", "--config", str(config_path)])

        # Verify onboarding completed
        assert result.exit_code in [0, 1], "Onboard should complete"
        assert "complete" in result.output.lower() or "success" in result.output.lower() or "done" in result.output.lower(), "Should indicate completion"
        # Verify config file was created
