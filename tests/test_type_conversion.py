from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple

import pytest

import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_optional():
    app = typer.Typer()

    @app.command()
    def opt(user: Optional[str] = None):
        if user:
            typer.echo(f"User: {user}")
        else:
            typer.echo("No user")

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "No user" in result.output

    result = runner.invoke(app, ["--user", "Camila"])
    assert result.exit_code == 0
    assert "User: Camila" in result.output


def test_optional_tuple():
    app = typer.Typer()
    values = []

    @app.command()
    def main(numbers: Optional[Tuple[int, int]] = None):
        values.append(numbers)

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert values == [None]

    result = runner.invoke(app, ["--numbers", "4", "2"])
    assert result.exit_code == 0, result.output
    assert values == [None, (4, 2)]


@pytest.mark.parametrize("declaration", [typer.Argument, typer.Option])
def test_optional_tuple_callback_returns_none(declaration):
    app = typer.Typer()
    callback_values = []
    command_values = []

    def callback(value):
        callback_values.append(value)
        return None

    @app.command()
    def main(
        numbers: Optional[Tuple[int, int]] = declaration(None, callback=callback),
    ):
        command_values.append(numbers)

    for args, expected in [([], None), (["4", "2"], (4, 2))]:
        if args and declaration is typer.Option:
            args.insert(0, "--numbers")
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert callback_values[-1] == expected
        assert command_values[-1] is None


def test_no_type():
    app = typer.Typer()

    @app.command()
    def no_type(user):
        typer.echo(f"User: {user}")

    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "User: Camila" in result.output


class SomeEnum(Enum):
    ONE = "one"
    TWO = "two"
    THREE = "three"


@pytest.mark.parametrize(
    "type_annotation",
    [List[Path], List[SomeEnum], List[str]],
)
def test_list_parameters_convert_to_lists(type_annotation):
    # Lists containing objects that are converted by Click (i.e. not Path or Enum)
    # should not be inadvertently converted to tuples
    expected_element_type = type_annotation.__args__[0]
    app = typer.Typer()

    @app.command()
    def list_conversion(container: type_annotation):
        assert isinstance(container, list)
        for element in container:
            assert isinstance(element, expected_element_type)

    result = runner.invoke(app, ["one", "two", "three"])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "type_annotation",
    [
        Tuple[str, str],
        Tuple[str, Path],
        Tuple[Path, Path],
        Tuple[str, SomeEnum],
        Tuple[SomeEnum, SomeEnum],
    ],
)
def test_tuple_parameter_elements_are_converted_recursively(type_annotation):
    # Tuple elements that aren't converted by Click (i.e. Path or Enum)
    # should be recursively converted by Typer
    expected_element_types = type_annotation.__args__
    app = typer.Typer()

    @app.command()
    def tuple_recursive_conversion(container: type_annotation):
        assert isinstance(container, tuple)
        for element, expected_type in zip(container, expected_element_types):
            assert isinstance(element, expected_type)

    result = runner.invoke(app, ["one", "two"])
    assert result.exit_code == 0


def test_callback():
    app = typer.Typer()

    def value_callback(value: Optional[SomeEnum]):
        typer.echo(f"Value: {value}")

    @app.command()
    def main(value: Optional[SomeEnum] = typer.Option(..., callback=value_callback)):
        pass

    result = runner.invoke(app, ["--value", "one"])
    assert result.exit_code == 0
    assert "Value: SomeEnum.ONE" in result.output
