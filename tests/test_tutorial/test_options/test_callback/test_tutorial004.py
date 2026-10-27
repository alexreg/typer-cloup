import os
import subprocess

import typer_cloup as typer
from docs_src.options.callback import tutorial004 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_1():
    result = runner.invoke(app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Validating param: name" in result.output
    assert "Hello Camila" in result.output


def test_2():
    result = runner.invoke(app, ["--name", "rick"])
    assert result.exit_code != 0
    assert "Error: Invalid value for '--name'" in result.output
    assert "Only Camila is allowed" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout


def test_completion():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL004.PY_COMPLETE": "bash_complete",
            "COMP_WORDS": "tutorial004.py --",
            "COMP_CWORD": "1",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "--name" in result.stdout
