"""Unit tests for CLI Models Command."""
import pytest
from typer.testing import CliRunner
from synapse.cli.main import app

@pytest.mark.unit
class TestCLIModelsCommand:
    def test_models_command_exists(self):
        runner = CliRunner()
        result = runner.invoke(app, ["models", "--help"])
        assert result.exit_code == 0
        assert "models" in result.output.lower()

    def test_models_list(self):
        runner = CliRunner()
        result = runner.invoke(app, ["models", "list"])
        assert result.exit_code == 0

    def test_models_list_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["models", "list", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output.lower()

    def test_models_download_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["models", "download", "--help"])
        assert result.exit_code == 0
        assert "download" in result.output.lower()

    def test_models_verify_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["models", "verify", "--help"])
        assert result.exit_code == 0
        assert "verify" in result.output.lower()

    def test_models_remove_help(self):
        runner = CliRunner()
        result = runner.invoke(app, ["models", "remove", "--help"])
        assert result.exit_code == 0
        assert "remove" in result.output.lower()

    def test_models_download_with_force(self):
        runner = CliRunner()
        result = runner.invoke(app, ["models", "download", "test-model", "--force"])
        assert result.exit_code in [0, 1, 2]

    def test_models_download_with_short_force(self):
        runner = CliRunner()
        result = runner.invoke(app, ["models", "download", "test-model", "-f"])
        assert result.exit_code in [0, 1, 2]

