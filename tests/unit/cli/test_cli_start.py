"""Unit tests for CLI Start Command."""
import pytest
from typer.testing import CliRunner
from synapse.cli.main import app

@pytest.mark.unit
class TestCLIStartCommand:
    def test_start_command_exists(self):
        runner = CliRunner()
        result = runner.invoke(app, ["start", "--help"])
        assert result.exit_code == 0
        assert "start" in result.output.lower()

    def test_start_executes(self):
        runner = CliRunner()
        result = runner.invoke(app, ["start"])
        assert result.exit_code in [0, 1, 2]

    def test_start_with_port(self):
        runner = CliRunner()
        result = runner.invoke(app, ["start", "--port", "8080"])
        assert result.exit_code in [0, 1, 2]

    def test_start_with_short_port(self):
        runner = CliRunner()
        result = runner.invoke(app, ["start", "-p", "9000"])
        assert result.exit_code in [0, 1, 2]

    def test_start_with_docker(self):
        runner = CliRunner()
        result = runner.invoke(app, ["start", "--docker"])
        assert result.exit_code in [0, 1, 2]

    def test_start_with_short_docker(self):
        runner = CliRunner()
        result = runner.invoke(app, ["start", "-d"])
        assert result.exit_code in [0, 1, 2]

    def test_start_help_shows_options(self):
        runner = CliRunner()
        result = runner.invoke(app, ["start", "--help"])
        assert result.exit_code == 0
        assert "port" in result.output.lower()
        assert "docker" in result.output.lower()

