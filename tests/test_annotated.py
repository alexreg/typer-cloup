from pathlib import Path
from typing import Annotated

import click
import cloup
import pytest

import typer_cloup as typer
from docs_src.annotated import tutorial001
from typer_cloup import utils
from typer_cloup.main import get_command
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_option_aliases_preserve_metadata():
    group = cloup.OptionGroup("Counts")
    value_type = click.IntRange(1, 10)
    option = typer.Option(
        "--count", "-c", group=group, type=value_type, help="Count items"
    )
    annotation = Annotated[int, "unrelated metadata", option]
    app = typer.Typer()

    @app.command()
    def main(value: annotation = 2):
        typer.echo(value)
        return value

    def other(value: annotation = 5):
        return value

    for args, expected in [
        ([], "2\n"),
        (["-c", "3"], "3\n"),
        (["--count", "4"], "4\n"),
    ]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert result.output == expected

    result = runner.invoke(app, ["--count", "11"])
    assert result.exit_code == 2
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Counts:" in result.output
    assert "Count items" in result.output
    assert "--count" in result.output
    parameter = get_command(app).params[0]
    assert parameter.group is group
    assert parameter.type is value_type
    assert option.default == "--count"
    assert option.param_decls == ("-c",)
    assert main() == 2
    assert other() == 5
    assert utils.get_params_from_function(other)["value"].default.default == 5
    assert utils.get_params_from_function(main)["value"].default.default == 2


@pytest.mark.parametrize(
    "kind", ["required-option", "required-argument", "optional-argument"]
)
def test_required_and_optional_parameters(kind):
    declaration = typer.Option if kind == "required-option" else typer.Argument
    annotation = Annotated[str, declaration(help="Display name")]
    app = typer.Typer()

    if kind == "optional-argument":

        def main(name: annotation = "World"):
            typer.echo(name)

    else:

        def main(name: annotation):
            typer.echo(name)

    app.command()(main)
    result = runner.invoke(app)
    assert result.exit_code == (0 if kind == "optional-argument" else 2)
    if kind == "optional-argument":
        assert result.output == "World\n"
    args = ["--name", "Camila"] if kind == "required-option" else ["Camila"]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    assert result.output == "Camila\n"


@pytest.mark.parametrize("kind", ["list", "shell-quoted-list", "tuple"])
def test_optional_container_conversion(kind):
    values = []

    def callback(value):
        values.append(value)
        return value

    option = typer.Option(
        callback=callback, shell_quoted_list=kind == "shell-quoted-list"
    )
    base = tuple[Path, int] | None if kind == "tuple" else list[Path] | None
    annotation = Annotated[base, option]
    app = typer.Typer()

    @app.command()
    def main(paths: annotation = None):
        assert paths == values[-1]

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert values == [None]
    if kind == "tuple":
        args, expected = ["--paths", "one", "2"], (Path("one"), 2)
    elif kind == "shell-quoted-list":
        args, expected = ["--paths", "'one file' two"], [Path("one file"), Path("two")]
    else:
        args, expected = ["--paths", "one", "--paths", "two"], [
            Path("one"),
            Path("two"),
        ]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    assert values == [None, expected]


def test_unrelated_metadata_with_legacy_declaration():
    app = typer.Typer()

    @app.command()
    def main(value: Annotated[int, "unrelated metadata"] = typer.Option(1, "--number")):
        typer.echo(value)

    result = runner.invoke(app, ["--number", "2"])
    assert result.exit_code == 0, result.output
    assert result.output == "2\n"


def test_documented_postponed_annotations():
    app = typer.Typer()
    app.command()(tutorial001.main)
    result = runner.invoke(app, ["Camila", "--label", "Welcome"])
    assert result.exit_code == 0, result.output
    assert result.output == "Welcome, Camila!\n"
    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert result.output == "Hello, World!\n"
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[NAME]" in result.output
    assert "Person to greet" in result.output
    assert "Greeting text" in result.output


@pytest.mark.parametrize(
    "annotated", [True, False], ids=["annotated-option", "legacy-argument"]
)
def test_default_factory(annotated):
    calls = []

    def factory():
        calls.append(None)
        return len(calls)

    declaration = typer.Option if annotated else typer.Argument
    parameter = declaration(default_factory=factory)
    app = typer.Typer()

    if annotated:

        def main(value: Annotated[int, parameter]):
            typer.echo(value)

    else:

        def main(value: int = parameter):
            typer.echo(value)

    app.command()(main)

    for expected in ["1\n", "2\n"]:
        result = runner.invoke(app)
        assert result.exit_code == 0, result.output
        assert result.output == expected
    args = ["--value", "9"] if annotated else ["9"]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    assert result.output == "9\n"
    assert len(calls) == 2
    assert parameter.default is ...


@pytest.mark.parametrize(
    "kind, error, message",
    [
        ("multiple", "MultipleTyperAnnotationsError", "multiple"),
        ("mixed", "MixedAnnotatedAndDefaultStyleError", "together"),
        ("argument-default", "AnnotatedParamWithDefaultValueError", "with `=`"),
        ("annotated-factory", "DefaultFactoryAndDefaultValueError", "default_factory"),
        ("legacy-factory", "DefaultFactoryAndDefaultValueError", "default_factory"),
    ],
)
def test_invalid_declarations(kind, error, message):
    annotation = str
    default = ...
    if kind == "multiple":
        annotation = Annotated[str, typer.Option(), typer.Argument()]
    elif kind == "mixed":
        annotation = Annotated[str, typer.Argument()]
        default = typer.Option("value")
    elif kind == "argument-default":
        annotation = Annotated[str, typer.Argument("value")]
    elif kind == "annotated-factory":
        annotation = Annotated[str, typer.Option(default_factory=lambda: "value")]
        default = None
    elif kind == "legacy-factory":
        default = typer.Argument("value", default_factory=lambda: "value")
    app = typer.Typer()

    @app.command()
    def main(value: annotation = default):
        pytest.fail("Invalid declaration reached command")

    with pytest.raises(getattr(utils, error), match=message):
        runner.invoke(app)
