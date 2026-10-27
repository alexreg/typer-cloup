import subprocess

import typer_cloup as typer
from docs_src.parameter_types.enum import tutorial001 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--network [simple|conv|lstm]" in result.output


def test_main():
    result = runner.invoke(app, ["--network", "conv"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_invalid():
    result = runner.invoke(app, ["--network", "capsule"])
    assert result.exit_code != 0
    assert "Error: Invalid value for '--network'" in result.output
    assert "'capsule' is not one of 'simple', 'conv', 'lstm'" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
