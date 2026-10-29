import subprocess
import sys

import typer_cloup as typer
from docs_src.first_steps import tutorial001 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_cli():
    app = typer.Typer()
    app.command()(mod.main)
    result = runner.invoke(app, [])
    assert result.output == "Hello World\n"


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
