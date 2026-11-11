from typing import List, Optional

import pytest

import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()


@pytest.mark.parametrize("declaration", [typer.Argument, typer.Option])
def test_optional_list_preserves_none(declaration):
    app = typer.Typer()
    callback_values = []
    command_values = []

    def callback(value):
        callback_values.append(value)
        return [item.upper() for item in value] if value is not None else None

    @app.command()
    def main(values: Optional[List[str]] = declaration(None, callback=callback)):
        command_values.append(values)

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert callback_values == [None]
    assert command_values == [None]

    args = ["one", "two"]
    if declaration is typer.Option:
        args = ["--values", "one", "--values", "two"]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    assert callback_values == [None, ["one", "two"]]
    assert command_values == [None, ["ONE", "TWO"]]


def test_shell_quoted_optional_list():
    app = typer.Typer()
    values = []

    @app.command()
    def main(names: Optional[List[str]] = typer.Argument(None, shell_quoted_list=True)):
        values.append(names)

    for args, expected in [
        ([], None),
        (["'Joe Bloggs' Camila"], ["Joe Bloggs", "Camila"]),
    ]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert values[-1] == expected


@pytest.mark.parametrize("default", [[], list], ids=["empty", "empty-factory"])
def test_empty_list_defaults_are_preserved(default):
    app = typer.Typer()
    values = []

    @app.command()
    def main(numbers: List[int] = typer.Option(default)):
        values.append(numbers)

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert values == [[]]


@pytest.mark.parametrize("callback_result", [None, []])
def test_list_callback_can_clear_value(callback_result):
    app = typer.Typer()
    values = []

    def callback(value):
        assert value == ["provided"]
        return callback_result

    @app.command()
    def main(
        names: Optional[List[str]] = typer.Option(["default"], callback=callback),
    ):
        values.append(names)

    result = runner.invoke(app, ["--names", "provided"])
    assert result.exit_code == 0, result.output
    assert values == [callback_result]
