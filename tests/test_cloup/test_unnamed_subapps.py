import pytest
from click import Command
from cloup import Section

import typer_cloup as typer
from typer_cloup.testing import CliRunner

runner = CliRunner()


def test_unnamed_subapps_preserve_sections_and_aliases():
    app = typer.Typer(show_subcommand_aliases=True)
    child = typer.Typer()
    wrapper = typer.Typer()
    tools = typer.Typer()
    section = Section(
        "Greetings",
        commands=[Command("welcome", callback=lambda: typer.echo("welcome"))],
    )

    @app.command()
    def status():
        typer.echo("ready")

    @child.command(section=section, aliases=["hi"])
    def hello():
        """Say hello."""
        typer.echo("hello")

    @tools.command()
    def ping():
        typer.echo("pong")

    child.add_sub(tools, name="tools", aliases=["t"])
    wrapper.add_sub(child)
    app.add_sub(wrapper)

    for args, expected in [
        (["status"], "ready\n"),
        (["hello"], "hello\n"),
        (["hi"], "hello\n"),
        (["welcome"], "welcome\n"),
        (["tools", "ping"], "pong\n"),
        (["t", "ping"], "pong\n"),
    ]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output
        assert result.output == expected

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.output
    assert "Greetings:" in result.output
    assert "hello (hi)" in result.output
    assert "tools (t)" in result.output
    assert result.output.count("Say hello.") == 1
    assert list(section.commands) == ["welcome"]


def test_unnamed_subapp_replaces_parent_command():
    app = typer.Typer()
    child = typer.Typer()

    @app.command("hello", section=Section("Parent"), help="Old greeting")
    def original():
        pytest.fail("Replaced command was invoked")

    @child.command()
    def hello():
        """New greeting."""
        typer.echo("new")

    app.add_sub(child)
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0, result.output
    assert result.output == "new\n"
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.output
    assert "New greeting." in result.output
    assert "Old greeting" not in result.output
    assert "Parent:" not in result.output


def test_unnamed_subapp_warns_and_ignores_callback():
    app = typer.Typer()
    child = typer.Typer()
    callbacks = []

    @child.callback()
    def callback():
        callbacks.append(None)

    @child.command()
    def hello():
        typer.echo("hello")

    app.add_sub(child, name="")
    with pytest.warns(UserWarning, match="callback.*add_sub"):
        result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0, result.output
    assert result.output == "hello\n"
    assert callbacks == []
