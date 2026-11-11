from cloup import OptionGroup

import typer_cloup as typer
from typer_cloup.testing import CliRunner


def test_help_labels_use_gettext(monkeypatch):
    translations = {
        "Arguments": "Translated arguments",
        "Options": "Translated options",
        "env var: {var}": "environment: {var}",
        "default: {default}": "initial: {default}",
        "required": "mandatory",
        "(dynamic)": "(computed)",
    }
    monkeypatch.setattr(
        "typer_cloup.core._", lambda message: translations.get(message, message)
    )
    app = typer.Typer()
    custom_group = OptionGroup("Custom options")

    @app.command()
    def main(
        name: str = typer.Argument(..., help="Custom argument help"),
        suffix: str = typer.Argument("World", envvar="NAME_ENV"),
        count: int = typer.Option(default_factory=lambda: 2),
        mode: str = typer.Option(
            "normal", group=custom_group, help="Custom option help"
        ),
    ):
        pass

    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0, result.output
    assert "Translated arguments:" in result.output
    assert "Translated options:" in result.output
    assert "environment: NAME_ENV" in result.output
    assert "initial: World" in result.output
    assert "initial: (computed)" in result.output
    assert "mandatory" in result.output
    assert "Custom options:" in result.output
    assert "Custom argument help" in result.output
    assert "Custom option help" in result.output
