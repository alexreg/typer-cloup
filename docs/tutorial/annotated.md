# Parameter declarations with `Annotated`

Use `typing.Annotated` to keep CLI configuration in a parameter's type annotation
and its default value in the Python function signature:

```Python
{!../docs_src/annotated/tutorial001.py!}
```

Here, `typer.Argument()` makes `name` a positional argument, while
`typer.Option("--label", "-l")` gives `greeting` long and short option names.
The defaults are ordinary Python values, so calling `main()` directly uses
`"World"` and `"Hello"` too.

```console
$ python main.py
Hello, World!

$ python main.py Camila --label Welcome
Welcome, Camila!
```

With `Annotated`, every positional value passed to `typer.Option()` is an option
name. Set the parameter's default with `=`. Omitting the default makes the CLI
parameter required:

```Python
from typing import Annotated

import typer_cloup as typer


def main(name: Annotated[str, typer.Option("--name", "-n")]):
    typer.echo(name)
```

`Annotated` also supports the existing parameter settings, including `envvar`,
`callback`, `type`, `group`, and `shell_quoted_list`. For optional values, use an
annotation such as `str | None` and set the default to `None`. An annotation that
allows `None` does not by itself make a CLI parameter optional.

## Dynamic defaults

Use `default_factory` to compute a default when the CLI parameter is omitted:

```Python
from datetime import datetime
from typing import Annotated

import typer_cloup as typer


def current_year() -> int:
    return datetime.now().year


def main(year: Annotated[int, typer.Option(default_factory=current_year)]):
    typer.echo(year)
```

`default_factory` also works with declarations in the older style:

```Python
def main(year: int = typer.Option(default_factory=current_year)):
    typer.echo(year)
```

Existing callable defaults, such as `typer.Option(current_year)`, continue to
work. `default_factory` makes the intent explicit without putting a callable in
the function's default value when using `Annotated`.

## Declaration rules

Use at most one `typer.Option()` or `typer.Argument()` metadata object per
parameter. Other metadata is ignored by Typer-Cloup.

When using `Annotated`, set ordinary defaults with `=`, rather than inside
`typer.Argument()`. Do not also assign `typer.Option()` or `typer.Argument()` as
the function's default value. A parameter cannot have both an ordinary default
and `default_factory`.

Metadata can be reused across parameters. Each parameter gets its own copy of
the configuration, while objects such as Cloup option groups retain their
identity. Forward references and `from __future__ import annotations` are
supported.

The older declaration style, such as
`name: str = typer.Option("World", "--label")`, remains supported.
