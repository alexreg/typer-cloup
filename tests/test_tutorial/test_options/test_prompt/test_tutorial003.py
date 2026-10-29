import subprocess
import sys

import typer_cloup as typer
from docs_src.options.prompt import tutorial003 as mod
from typer_cloup.testing import CliRunner, columns_match

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_prompt():
    result = runner.invoke(app, input="Old Project\nOld Project\n")
    assert result.exit_code == 0
    assert "Deleting project Old Project" in result.output


def test_prompt_not_equal():
    result = runner.invoke(
        app, input="Old Project\nNew Spice\nOld Project\nOld Project\n"
    )
    assert result.exit_code == 0
    assert "Error: The two entered values do not match" in result.output
    assert "Deleting project Old Project" in result.output


def test_option():
    result = runner.invoke(app, ["--project-name", "Old Project"])
    assert result.exit_code == 0
    assert "Deleting project Old Project" in result.output
    assert "Project name: " not in result.output


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert columns_match(result.output, "--project-name TEXT", "[required]")


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
