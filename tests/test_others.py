import os
import subprocess
from pathlib import Path

import click
import pytest

import typer_cloup as typer
from typer_cloup.main import solve_typer_info_defaults, solve_typer_info_help
from typer_cloup.models import TyperInfo
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_help_from_info():
    # Mainly for coverage/completeness
    value = solve_typer_info_help(TyperInfo())
    assert value is None


def test_defaults_from_info():
    # Mainly for coverage/completeness
    value = solve_typer_info_defaults(TyperInfo())
    assert value


def test_install_invalid_shell():
    app = typer.Typer()

    @app.command()
    def main():
        pass  # pragma: no cover

    result = runner.invoke(app, env={"_MAIN_COMPLETE": "xshell_source"})
    assert "Shell 'xshell' is not supported." in result.output


def test_callback_too_many_parameters():
    app = typer.Typer()

    def name_callback(ctx, param, val1, val2):
        pass  # pragma: no cover

    @app.command()
    def main(name: str = typer.Option(..., callback=name_callback)):
        pass  # pragma: no cover

    with pytest.raises(click.ClickException) as exc_info:
        runner.invoke(app, ["--name", "Camila"])
    assert (
        exc_info.value.message == "Too many CLI parameter callback function parameters"
    )


def test_callback_2_untyped_parameters():
    app = typer.Typer()

    def name_callback(ctx, value):
        typer.echo(f"info name is: {ctx.info_name}")
        typer.echo(f"value is: {value}")

    @app.command()
    def main(name: str = typer.Option(..., callback=name_callback)):
        typer.echo("Hello World")

    result = runner.invoke(app, ["--name", "Camila"])
    assert "info name is: main" in result.stdout
    assert "value is: Camila" in result.stdout


def test_callback_3_untyped_parameters():
    app = typer.Typer()

    def name_callback(ctx, param, value):
        typer.echo(f"info name is: {ctx.info_name}")
        typer.echo(f"param name is: {param.name}")
        typer.echo(f"value is: {value}")

    @app.command()
    def main(name: str = typer.Option(..., callback=name_callback)):
        pass

    result = runner.invoke(app, ["--name", "Camila"])
    assert "info name is: main" in result.stdout
    assert "param name is: name" in result.stdout
    assert "value is: Camila" in result.stdout


def test_completion_untyped_parameters():
    file_path = Path(__file__).parent / "assets/completion_no_types.py"
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPLETION_NO_TYPES.PY_COMPLETE": "zsh_complete",
            "COMP_WORDS": "completion_no_types.py --name Sebastian --name Ca",
            "COMP_CWORD": "4",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "info name is: completion_no_types.py" in result.stderr
    assert "param is: name" in result.stderr
    assert "incomplete is: Ca" in result.stderr
    assert (
        "plain\nCamila\nThe reader of books.\n"
        "plain\nCarlos\nThe writer of scripts.\n"
        "plain\nSebastian\nThe type hints guy.\n" in result.stdout
    )

    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_completion_untyped_parameters_different_order_correct_names():
    file_path = Path(__file__).parent / "assets/completion_no_types_order.py"
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPLETION_NO_TYPES_ORDER.PY_COMPLETE": "zsh_complete",
            "COMP_WORDS": "completion_no_types.py --name Sebastian --name Ca",
            "COMP_CWORD": "4",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "info name is: completion_no_types_order.py" in result.stderr
    assert "param is: name" in result.stderr
    assert "incomplete is: Ca" in result.stderr
    assert (
        "plain\nCamila\nThe reader of books.\n"
        "plain\nCarlos\nThe writer of scripts.\n" in result.stdout
    )

    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_autocompletion_too_many_parameters():
    app = typer.Typer()

    def name_callback(ctx, param, incomplete, val2):
        pass  # pragma: no cover

    @app.command()
    def main(name: str = typer.Option(..., shell_complete=name_callback)):
        pass  # pragma: no cover

    with pytest.raises(click.ClickException) as exc_info:
        runner.invoke(app, ["--name", "Camila"])
    assert (
        exc_info.value.message == "Invalid shell-completion callback parameters: val2"
    )


def test_forward_references():
    app = typer.Typer()

    @app.command()
    def main(arg1, arg2: int, arg3: "int", arg4: bool = False, arg5: "bool" = False):
        typer.echo(f"arg1: {type(arg1)} {arg1}")
        typer.echo(f"arg2: {type(arg2)} {arg2}")
        typer.echo(f"arg3: {type(arg3)} {arg3}")
        typer.echo(f"arg4: {type(arg4)} {arg4}")
        typer.echo(f"arg5: {type(arg5)} {arg5}")

    result = runner.invoke(app, ["Hello", "2", "invalid"])

    assert (
        "Error: Invalid value for 'ARG3': 'invalid' is not a valid integer"
        in result.output
    )
    result = runner.invoke(app, ["Hello", "2", "3", "--arg4", "--arg5"])
    assert (
        "arg1: <class 'str'> Hello\narg2: <class 'int'> 2\narg3: <class 'int'> 3\narg4: <class 'bool'> True\narg5: <class 'bool'> True\n"
        in result.stdout
    )


def test_context_settings_inheritance_single_command():
    app = typer.Typer(context_settings=dict(help_option_names=["-h", "--help"]))

    @app.command()
    def main(name: str):
        pass  # pragma: no cover

    result = runner.invoke(app, ["main", "-h"])
    assert "Show this message and exit." in result.stdout


def test_invoke():
    app = typer.Typer()
    foo_app = typer.Typer(name="foo")

    app.add_sub(foo_app)

    @app.command()
    def invoke():
        app.invoke(hello)

    @app.command()
    def forward(name: str):
        app.forward(hello)

    @foo_app.command()
    def hello(name: str = "World"):
        typer.echo(f"Hello {name}")

    result = runner.invoke(app, ["invoke"])
    assert result.exit_code == 0
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["forward", "John"])
    assert result.exit_code == 0
    assert "Hello John" in result.stdout


def test_invoke_callback_not_command():
    app = typer.Typer()

    @app.command()
    def invoke():
        app.invoke(None)

    @app.command()
    def forward(name: str):
        app.forward(None)

    with pytest.raises(TypeError) as exc_info:
        runner.invoke(app, ["invoke"], catch_exceptions=False)
    assert exc_info.value.args[0] == "callback is not a command"

    with pytest.raises(TypeError) as exc_info:
        runner.invoke(app, ["forward", "John"], catch_exceptions=False)
    assert exc_info.value.args[0] == "callback is not a command"


def test_help_defaults():
    app = typer.Typer(context_settings=dict(auto_envvar_prefix="TEST"))

    @app.command()
    def main(
        name: str = typer.Option("John"),
        lastname: str = typer.Option("Doe", show_default="Mr. Doe"),
        age: int = typer.Option(lambda: 42, show_default=True),
    ):
        pass  # pragma: no cover

    result = runner.invoke(app, ["main", "--help"])
    assert result.exit_code == 0
    assert "John" in result.output
    assert "Mr. Doe" in result.output
    assert "(dynamic)" in result.output


def test_help_option_envvar():
    # Mainly for coverage/completeness
    app = typer.Typer()

    @app.command()
    def main(name: str = typer.Option("World", envvar="AWESOME_NAME")):
        typer.echo(f"Hello Mr. {name}")

    result = runner.invoke(app, env={"AWESOME_NAME": "Wednesday"})
    assert result.exit_code == 0
    assert "Hello Mr. Wednesday" in result.output


def test_help_slash_option():
    app = typer.Typer()

    @app.command()
    def main(name: str = typer.Option(..., "/name")):
        pass  # pragma: no cover

    result = runner.invoke(app, ["main", "--help"])
    assert result.exit_code == 0
    assert "/name TEXT" in result.output


def test_help_hidden_parameter():
    app = typer.Typer()

    @app.command()
    def main(
        name: str = typer.Argument(..., hidden=True),
        lastname: str = typer.Option(..., hidden=True),
    ):
        pass  # pragma: no cover

    result = runner.invoke(app, ["main", "--help"])
    assert result.exit_code == 0
    assert "  NAME" not in result.output
    assert "--lastname" not in result.output


def test_help_hidden_group():
    app = typer.Typer()

    @app.command()
    def main(
        name: str = typer.Argument(..., hidden=True),
        lastname: str = typer.Argument(..., hidden=True),
    ):
        pass  # pragma: no cover

    result = runner.invoke(app, ["main", "--help"])
    assert result.exit_code == 0
    assert "NAME" in result.output
    assert "LASTNAME" in result.output
    assert "Arguments:" not in result.output
