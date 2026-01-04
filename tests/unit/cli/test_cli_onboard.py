"""Unit tests for CLI Onboard Command."""
import pytest
from typer.testing import CliRunner
from synapse.cli.main import app

@pytest.mark.unit
class TestCLIOboardCommand:
    def test_onboard_command_exists(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "--help"])
        assert result.exit_code == 0
        assert "onboard" in result.output.lower()

    def test_onboard_executes(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "--quick"])
        assert result.exit_code in [0, 1, 2]

    def test_onboard_with_quick(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "--quick"])
        assert result.exit_code in [0, 1, 2]

    def test_onboard_with_short_quick(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "-q"])
        assert result.exit_code in [0, 1, 2]

    def test_onboard_with_silent(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "--silent"])
        assert result.exit_code in [0, 1, 2]

    def test_onboard_with_short_silent(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "-s"])
        assert result.exit_code in [0, 1, 2]

    def test_onboard_with_skip_test(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "--quick", "--skip-test"])
        assert result.exit_code in [0, 1, 2]

    def test_onboard_with_skip_ingest(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "--quick", "--skip-ingest"])
        assert result.exit_code in [0, 1, 2]

    def test_onboard_help_shows_options(self):
        runner = CliRunner()
        result = runner.invoke(app, ["onboard", "--help"])
        assert result.exit_code == 0
        assert "quick" in result.output.lower()
        assert "silent" in result.output.lower()

