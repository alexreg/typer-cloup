from __future__ import annotations

from typing import Annotated

import typer_cloup as typer


def main(
    name: Annotated[str, typer.Argument(help="Person to greet")] = "World",
    greeting: Annotated[
        str, typer.Option("--label", "-l", help="Greeting text")
    ] = "Hello",
):
    typer.echo(f"{greeting}, {name}!")


if __name__ == "__main__":
    typer.run(main)
