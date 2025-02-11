import subprocess

import typer_cloup as typer
from docs_src.parameter_types.number import tutorial002 as mod
from typer_cloup.testing import CliRunner

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_invalid_id():
    result = runner.invoke(app, ["1002"])
    assert result.exit_code != 0
    assert (
        "Error: Invalid value for 'ID': 1002 is not in the range 0<=x<=1000"
        in result.output
    )


def test_clamped():
    result = runner.invoke(app, ["5", "--rank", "11", "--score", "-5"])
    assert result.exit_code == 0
    assert "ID is 5" in result.output
    assert "--rank is 10" in result.output
    assert "--score is 0" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
