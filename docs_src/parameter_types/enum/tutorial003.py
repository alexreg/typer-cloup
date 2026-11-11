from typing import Annotated, Literal

import typer_cloup as typer


def main(
    network: Annotated[Literal["simple", "conv", "lstm"], typer.Option()] = "simple",
):
    typer.echo(f"Training neural network of type: {network}")


if __name__ == "__main__":
    typer.run(main)
