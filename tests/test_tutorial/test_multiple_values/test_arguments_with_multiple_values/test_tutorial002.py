import subprocess
import sys

import typer_cloup as typer
from docs_src.multiple_values.arguments_with_multiple_values import tutorial002 as mod
from typer_cloup.testing import CliRunner, columns_match

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAMES]..." in result.output
    assert "Arguments:" in result.output
    assert columns_match(
        result.output,
        "[NAMES]...",
        "Select 3 characters to play with  [default: Harry, Hermione, Ron]",
    )


def test_defaults():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello Harry" in result.output
    assert "Hello Hermione" in result.output
    assert "Hello Ron" in result.output


def test_invalid_args():
    result = runner.invoke(app, ["Draco", "Hagrid"])
    assert result.exit_code != 0
    assert "Error: Argument 'names' takes 3 values" in result.output


def test_valid_args():
    result = runner.invoke(app, ["Draco", "Hagrid", "Dobby"])
    assert result.exit_code == 0
    assert "Hello Draco" in result.stdout
    assert "Hello Hagrid" in result.stdout
    assert "Hello Dobby" in result.stdout


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
