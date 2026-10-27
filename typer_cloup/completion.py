from typing import Any, MutableMapping

import click
import click.exceptions
import click.shell_completion
from click.shell_completion import get_completion_class


# Re-implement `shell_complete` to add error messages.
def shell_complete(
    cli: click.Command,
    ctx_args: MutableMapping[str, Any],
    prog_name: str,
    complete_var: str,
    instruction: str,
) -> int:
    if "_" not in instruction:
        click.echo("Invalid completion instruction.", err=True)
        return 1

    shell, _, instruction = instruction.partition("_")
    comp_cls = get_completion_class(shell)
    if comp_cls is None:
        click.echo(f"Shell '{shell}' is not supported.", err=True)
        return 1

    comp = comp_cls(cli, ctx_args, prog_name, complete_var)

    if instruction == "source":
        click.echo(comp.source())
        return 0
    elif instruction == "complete":
        click.echo(comp.complete())
        return 0

    click.echo(f"Completion instruction '{instruction}' is not supported.", err=True)
    return 1
