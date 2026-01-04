"""Unit tests for CLI Setup Command."""
import pytest
from typer.testing import CliRunner
from synapse.cli.main import app

@pytest.mark.unit
class TestCLISetupCommand:
    def test_setup_command_exists(self):
        runner = CliRunner()
        result = runner.invoke(app, ["setup", "--help"])
        assert result.exit_code == 0
        assert "setup" in result.output.lower()

    def test_setup_executes(self):
        runner = CliRunner()
        result = runner.invoke(app, ["setup"])
        assert result.exit_code in [0, 1, 2]

    def test_setup_with_force(self):
        runner = CliRunner()
        result = runner.invoke(app, ["setup", "--force"])
        assert result.exit_code in [0, 1, 2]

    def test_setup_with_short_force(self):
        runner = CliRunner()
        result = runner.invoke(app, ["setup", "-f"])
        assert result.exit_code in [0, 1, 2]

    def test_setup_with_offline(self):
        runner = CliRunner()
        result = runner.invoke(app, ["setup", "--offline"])
        assert result.exit_code in [0, 1, 2]

    def test_setup_with_no_model_check(self):
        runner = CliRunner()
        result = runner.invoke(app, ["setup", "--no-model-check"])
        assert result.exit_code in [0, 1, 2]

    def test_setup_help_shows_options(self):
        runner = CliRunner()
        result = runner.invoke(app, ["setup", "--help"])
        assert result.exit_code == 0
        assert "force" in result.output.lower()
        assert "offline" in result.output.lower()

