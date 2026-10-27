from enum import Enum
from typing import Optional

import click
import pytest
from click.testing import CliRunner as ClickCliRunner

import typer_cloup as typer
from typer_cloup.core import TyperArgument, TyperCommand, TyperOption
from typer_cloup.testing import CliRunner


@pytest.mark.parametrize("help", [None, "Native argument"])
def test_native_argument_help(help):
    argument = click.Argument(["name"], help=help)
    command = TyperCommand("main", params=[argument])
    result = ClickCliRunner().invoke(command, ["--help"])
    assert result.exit_code == 0, result.output
    assert "Arguments:" in result.output
    assert "NAME" in result.output
    if help:
        assert help in result.output


@pytest.mark.parametrize("default", [False, True])
def test_boolean_flag_defaults(default):
    app = typer.Typer()

    @app.command()
    def main(enabled: bool = default):
        typer.echo(str(enabled))

    runner = CliRunner()
    for args, expected in [
        ([], default),
        (["--enabled"], True),
        (["--no-enabled"], False),
    ]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert result.output.strip() == str(expected)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.output
    expected_default = "enabled" if default else "no-enabled"
    assert f"[default: {expected_default}]" in result.output


def test_explicit_flag_value():
    option = TyperOption(["--upper"], is_flag=True, flag_value="upper")
    command = click.Command(
        "main", params=[option], callback=lambda upper: typer.echo(upper)
    )
    result = ClickCliRunner().invoke(command, ["--upper"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == "upper"


def test_boolean_option_with_value():
    app = typer.Typer()

    @app.command()
    def main(enabled: bool = typer.Option(False, is_flag=False)):
        typer.echo(str(enabled))

    result = CliRunner().invoke(app, ["--enabled", "true"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == "True"


@pytest.mark.parametrize(
    "param_class, declaration, expected",
    [(TyperArgument, "name", "[NAME]"), (TyperOption, "--name", "TEXT")],
)
def test_metavar_with_optional_context(param_class, declaration, expected):
    param = param_class(
        param_decls=[declaration], type=click.STRING, required=False, nargs=1
    )
    ctx = click.Context(click.Command("main"))
    assert param.make_metavar(ctx) == expected
    assert param.make_metavar() == param.make_metavar(ctx)


def test_argument_metavar_legacy_custom_type():
    class LegacyType(click.ParamType):
        def get_metavar(self, param):
            return "LEGACY"

    param = TyperArgument(param_decls=["name"], type=LegacyType(), required=False)
    assert param.make_metavar() == "[NAME]:LEGACY"


def test_argument_metavar_passes_context():
    ctx = click.Context(click.Command("main"))

    class ContextType(click.ParamType):
        def get_metavar(self, param, ctx):
            return ctx.command.name.upper()

    param = TyperArgument(param_decls=["name"], type=ContextType(), required=False)
    assert param.make_metavar(ctx) == "[NAME]:MAIN"


@pytest.mark.parametrize(
    "param_class, declaration", [(TyperArgument, "name"), (TyperOption, "--name")]
)
def test_missing_parameter_values(param_class, declaration):
    param = param_class(param_decls=[declaration], required=False)
    ctx = click.Context(click.Command("main"))
    missing, _ = click.Option(["--name"]).consume_value(ctx, {})
    assert param.value_is_missing(missing)
    assert param.value_is_missing(None)
    assert not param.value_is_missing("")
    assert not param.value_is_missing(False)
    assert not param.value_is_missing(0)
    assert not param.value_is_missing(())
    param.nargs = 2
    assert param.value_is_missing(())


@pytest.mark.parametrize("option", [False, True])
def test_missing_required_parameter(option):
    app = typer.Typer()
    declaration = typer.Option(...) if option else typer.Argument(...)

    @app.command()
    def main(name: str = declaration):
        pytest.fail("Missing required parameter reached callback")

    result = CliRunner().invoke(app)
    assert result.exit_code == 2, result.output
    assert "Missing" in result.output


def test_optional_parameter_callback_receives_none():
    app = typer.Typer()
    values = []

    def callback(value):
        values.append(value)
        return value

    @app.command()
    def main(name: Optional[str] = typer.Option(None, callback=callback)):
        assert name is None

    result = CliRunner().invoke(app)
    assert result.exit_code == 0, result.output
    assert values == [None]


@pytest.mark.parametrize("case_sensitive", [False, True])
def test_enum_defaults_and_normalized_values(case_sensitive):
    class User(str, Enum):
        RICK = "Rick"
        MORTY = "Morty"

    app = typer.Typer(context_settings={"token_normalize_func": str.lower})

    @app.command()
    def main(user: User = typer.Option(User.RICK, case_sensitive=case_sensitive)):
        typer.echo(user.value)

    runner = CliRunner()
    for args, expected in [([], "Rick"), (["--user", "MORTY"], "Morty")]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert result.output.strip() == expected
