from enum import Enum

import pytest

import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()


class Case(Enum):
    UPPER = "A"
    LOWER = "a"


@pytest.mark.parametrize("declaration", [typer.Argument, typer.Option])
def test_enum_values_preserve_case(declaration):
    app = typer.Typer()
    values = []

    @app.command()
    def main(value: Case = declaration(...)):
        values.append(value)

    for raw, expected in [("A", Case.UPPER), ("a", Case.LOWER)]:
        args = ["--value", raw] if declaration is typer.Option else [raw]
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert values[-1] is expected


def test_enum_callback_preserves_member():
    app = typer.Typer()
    values = []

    def callback(value):
        assert isinstance(value, Case)
        return value

    @app.command()
    def main(value: Case = typer.Option(Case.UPPER, callback=callback)):
        values.append(value)

    for args, expected in [([], Case.UPPER), (["--value", "a"], Case.LOWER)]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert values[-1] is expected


@pytest.mark.parametrize("case_sensitive", [False, True])
def test_enum_case_sensitivity(case_sensitive):
    class MixedCase(Enum):
        ALPHA = "Alpha"

    app = typer.Typer()
    values = []

    @app.command()
    def main(value: MixedCase = typer.Option(..., case_sensitive=case_sensitive)):
        values.append(value)

    result = runner.invoke(app, ["--value", "aLpHa"])
    if case_sensitive:
        assert result.exit_code == 2, result.output
        assert "Invalid value for '--value'" in result.output
        assert values == []
    else:
        assert result.exit_code == 0, result.output
        assert values == [MixedCase.ALPHA]
