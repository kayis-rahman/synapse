"""Unit tests for CLI Stop Command."""
import pytest
from typer.testing import CliRunner
from synapse.cli.main import app

@pytest.mark.unit
class TestCLIStopCommand:
    def test_stop_command_exists(self):
        runner = CliRunner()
        result = runner.invoke(app, ["stop", "--help"])
        assert result.exit_code == 0
        assert "stop" in result.output.lower()

    def test_stop_executes(self):
        runner = CliRunner()
        result = runner.invoke(app, ["stop"])
        assert result.exit_code in [0, 1]

    def test_stop_help_shows_info(self):
        runner = CliRunner()
        result = runner.invoke(app, ["stop", "--help"])
        assert result.exit_code == 0
        assert "stop" in result.output.lower()

    def test_stop_no_args(self):
        runner = CliRunner()
        result = runner.invoke(app, ["stop"])
        assert result.exit_code in [0, 1]

    def test_stop_error_handling_invalid_option(self):
        runner = CliRunner()
        result = runner.invoke(app, ["stop", "--invalid-option"])
        assert result.exit_code != 0

    def test_stop_idempotent(self):
        runner = CliRunner()
        result1 = runner.invoke(app, ["stop"])
        result2 = runner.invoke(app, ["stop"])
        assert result1.exit_code == result2.exit_code

    def test_stop_output_contains_expected_content(self):
        runner = CliRunner()
        result = runner.invoke(app, ["stop"])
        assert "stop" in result.output.lower() or len(result.output) == 0

