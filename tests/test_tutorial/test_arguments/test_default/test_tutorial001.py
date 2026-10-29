import subprocess
import sys

import typer_cloup as typer
from docs_src.arguments.default import tutorial001 as mod
from typer_cloup.testing import CliRunner, columns_match

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAME]" in result.output
    assert "Arguments:" in result.output
    assert columns_match(result.output, "[NAME]", "[default: Wade Wilson]")


def test_call_no_arg():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello Wade Wilson" in result.output


def test_call_arg():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
