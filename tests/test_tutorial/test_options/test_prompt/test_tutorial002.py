import subprocess
import sys

import typer_cloup as typer
from docs_src.options.prompt import tutorial002 as mod
from typer_cloup.testing import CliRunner, columns_match

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_option_lastname():
    result = runner.invoke(app, ["Camila", "--lastname", "Gutiérrez"])
    assert result.exit_code == 0
    assert "Hello Camila Gutiérrez" in result.output


def test_option_lastname_prompt():
    result = runner.invoke(app, ["Camila"], input="Gutiérrez")
    assert result.exit_code == 0
    assert "Please tell me your last name: " in result.output
    assert "Hello Camila Gutiérrez" in result.output


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert columns_match(result.output, "--lastname TEXT", "[required]")


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
