The same as before, you can add help for the commands in the docstrings and the *CLI options*.

And the `typer.Typer()` application receives a parameter `help` that you can pass with the main help text for your CLI program:

```Python hl_lines="3  8 9 10  20  23 24 25 26 27  39  42 43 44 45 46  55 56 57"
{!../docs_src/commands/help/tutorial001.py!}
```

Check it:

<div class="termy">

```console
// Check the new help
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Awesome CLI user manager.

Options:
  --help  Show this message and exit.

Commands:
  create      Create a new user with USERNAME.
  delete      Delete a user with USERNAME.
  delete-all  Delete ALL users in the database.
  init        Initialize the users database.

// Now the commands have inline help 🎉

// Check the help for create
$ python main.py create --help

Usage: main.py create [OPTIONS] USERNAME

  Create a new user with USERNAME.

Options:
  --help  Show this message and exit.

// Check the help for delete
$ python main.py delete --help

Usage: main.py delete [OPTIONS] USERNAME

  Delete a user with USERNAME.

  If --force is not used, will ask for confirmation.

Options:
  --force / --no-force  Force deletion without confirmation.  [required]
  --help                Show this message and exit.

// Check the help for delete-all
$ python main.py delete-all --help

Usage: main.py delete-all [OPTIONS]

  Delete ALL users in the database.

  If --force is not used, will ask for confirmation.

Options:
  --force / --no-force  Force deletion without confirmation.  [required]
  --help                Show this message and exit.

// Check the help for init
$ python main.py init --help

Usage: main.py init [OPTIONS]

  Initialize the users database.

Options:
  --help  Show this message and exit.
```

</div>

!!! tip
    `typer.Typer()` receives several other parameters for other things, we'll see that later.

    You will also see how to use "Callbacks" later, and those include a way to add this same help message in a function docstring.

## Overwrite command help

You will probably be better adding the help text as a docstring to your functions, but if for some reason you wanted to overwrite it, you can use the `help` function argument passed to `@app.command()`:

```Python hl_lines="6  14"
{!../docs_src/commands/help/tutorial002.py!}
```

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

// Notice it uses the help passed to @app.command()
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new user with USERNAME.
  delete  Delete a user with USERNAME.

// It uses "Create a new user with USERNAME." instead of "Some internal utility function to create."
```

</div>

## Deprecate a Command

There could be cases where you have a command in your app that you need to deprecate, so that your users stop using it, even while it's still supported for a while.

You can mark it with the parameter `deprecated=True`:

```Python hl_lines="14"
{!../docs_src/commands/help/tutorial003.py!}
```

And when you show the `--help` option you will see it's marked as "`deprecated`":

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create a user.
  delete  (Deprecated) Delete a user.
```

</div>

And if you check the `--help` for the deprecated command (in this example, the command `delete`), it also shows it as deprecated:

<div class="termy">

```console
$ python main.py delete --help

Usage: main.py delete [OPTIONS] USERNAME

  (DEPRECATED) Delete a user.

  This is deprecated and will stop being supported soon.

Arguments:
  USERNAME  [required]

Options:
  --help    Show this message and exit.
```

</div>
