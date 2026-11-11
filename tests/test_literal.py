from typing import Literal

import pytest

import typer_cloup as typer
from docs_src.parameter_types.enum import tutorial003
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_documented_annotated_choices():
    app = typer.Typer()
    app.command()(tutorial003.main)

    for args, expected in [([], "simple"), (["--network", "conv"], "conv")]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert result.output == f"Training neural network of type: {expected}\n"

    result = runner.invoke(app, ["--network", "capsule"])
    assert result.exit_code == 2
    assert "Invalid value for '--network'" in result.output
    for choice in ["simple", "conv", "lstm"]:
        assert choice in result.output

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--network [simple|conv|lstm]" in result.output
    assert "[default: simple]" in result.output


def test_integer_argument_choices():
    app = typer.Typer()
    values = []

    @app.command()
    def main(level: Literal[1, 2] = typer.Argument(...)):
        values.append(level)

    result = runner.invoke(app, ["2"])
    assert result.exit_code == 0, result.output
    assert values == [2]
    assert type(values[0]) is int

    result = runner.invoke(app, ["3"])
    assert result.exit_code == 2
    assert "Invalid value" in result.output
    assert values == [2]

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "{1|2}" in result.output


@pytest.mark.parametrize("case_sensitive", [True, False])
def test_choice_case_sensitivity(case_sensitive):
    app = typer.Typer()
    values = []

    @app.command()
    def main(
        size: Literal["Large", "small"] = typer.Option(
            ..., case_sensitive=case_sensitive
        )
    ):
        values.append(size)

    result = runner.invoke(app, ["--size", "large"])
    assert result.exit_code == (2 if case_sensitive else 0), result.output
    assert values == ([] if case_sensitive else ["Large"])

    result = runner.invoke(app, ["--size", "Large"])
    assert result.exit_code == 0, result.output
    assert values[-1] == "Large"


def test_optional_choices():
    app = typer.Typer()
    values = []

    @app.command()
    def main(size: Literal["small", "large"] | None = None):
        values.append(size)

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert values == [None]

    result = runner.invoke(app, ["--size", "large"])
    assert result.exit_code == 0, result.output
    assert values == [None, "large"]
