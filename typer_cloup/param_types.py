import shlex
from enum import Enum
from typing import Any, Optional, Sequence

import click


class TyperChoice(click.Choice):
    def normalize_choice(self, choice: Any, ctx: Optional[click.Context]) -> str:
        # Click 8.2 normalizes Enum names; Typer accepts their values instead.
        value = str(choice.value) if isinstance(choice, Enum) else str(choice)
        if ctx is not None and ctx.token_normalize_func is not None:
            value = ctx.token_normalize_func(value)
        if not self.case_sensitive:
            value = value.casefold()
        return value


class ShellQuotedList(click.ParamType):
    """Converts a shell-quoted string into a list of strings."""

    name = "shell-quoted-list"

    def convert(
        self,
        value: Any,
        param: Optional["click.Parameter"],
        ctx: Optional["click.Context"],
    ) -> Any:
        if value is None:
            return None
        elif isinstance(value, list):
            return value

        return shlex.split(value)

    def split_envvar_value(self, rv: str) -> Sequence[str]:
        return rv  # pragma: no cover

    def __repr__(self) -> str:
        return "SHELL-QUOTED LIST"


SHELL_QUOTED_LIST = ShellQuotedList()
