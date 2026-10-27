import inspect
from gettext import gettext as _
from importlib import metadata
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Type, Union, cast

import click
import cloup
import cloup.constraints

from .models import ArgumentInfo, CommandFunctionType, OptionInfo

if TYPE_CHECKING:  # pragma: no cover
    import click.shell_completion


def Option(
    # Parameter
    default: Optional[Any],
    *param_decls: str,
    type: Optional[Union[click.types.ParamType[Any], Any]] = None,
    callback: Optional[Callable[..., Any]] = None,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, List[str]]] = None,
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[List["click.shell_completion.CompletionItem"], List[str]],
        ]
    ] = None,
    # Option
    show_default: Union[bool, str, Callable[[], Union[bool, str]]] = True,
    prompt: Union[bool, str] = False,
    confirmation_prompt: bool = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = True,
    group: Optional[cloup.OptionGroup] = None,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[List[str]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, Type[str], Type[bytes]] = None,
    # Shell-Quoted List
    shell_quoted_list: bool = False,
) -> Any:
    """Specify an option."""

    return OptionInfo(
        # Parameter
        default=default,
        param_decls=param_decls,
        type=type,
        callback=callback,
        metavar=metavar,
        expose_value=expose_value,
        is_eager=is_eager,
        envvar=envvar,
        shell_complete=shell_complete,
        # Option
        show_default=show_default,
        prompt=prompt,
        confirmation_prompt=confirmation_prompt,
        prompt_required=prompt_required,
        hide_input=hide_input,
        is_flag=is_flag,
        flag_value=flag_value,
        count=count,
        allow_from_autoenv=allow_from_autoenv,
        help=help,
        hidden=hidden,
        show_choices=show_choices,
        show_envvar=show_envvar,
        group=group,
        # Choice
        case_sensitive=case_sensitive,
        # Numbers
        min=min,
        max=max,
        clamp=clamp,
        # DateTime
        formats=formats,
        # File
        mode=mode,
        encoding=encoding,
        errors=errors,
        lazy=lazy,
        atomic=atomic,
        # Path
        exists=exists,
        file_okay=file_okay,
        dir_okay=dir_okay,
        writable=writable,
        readable=readable,
        resolve_path=resolve_path,
        allow_dash=allow_dash,
        path_type=path_type,
        # Shell-Quoted List
        shell_quoted_list=shell_quoted_list,
    )


def Argument(
    # Parameter
    default: Optional[Any],
    *,
    type: Optional[Union[click.types.ParamType[Any], Any]] = None,
    callback: Optional[Callable[..., Any]] = None,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, List[str]]] = None,
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[List["click.shell_completion.CompletionItem"], List[str]],
        ]
    ] = None,
    # TyperArgument
    show_default: Union[bool, str, Callable[[], Union[bool, str]]] = True,
    show_choices: bool = True,
    show_envvar: bool = True,
    allow_from_autoenv: bool = False,
    help: Optional[str] = None,
    hidden: bool = False,
    # Choice
    case_sensitive: bool = True,
    # Numbers
    min: Optional[Union[int, float]] = None,
    max: Optional[Union[int, float]] = None,
    clamp: bool = False,
    # DateTime
    formats: Optional[List[str]] = None,
    # File
    mode: Optional[str] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = "strict",
    lazy: Optional[bool] = None,
    atomic: bool = False,
    # Path
    exists: bool = False,
    file_okay: bool = True,
    dir_okay: bool = True,
    writable: bool = False,
    readable: bool = True,
    resolve_path: bool = False,
    allow_dash: bool = False,
    path_type: Union[None, Type[str], Type[bytes]] = None,
    # Shell-Quoted List
    shell_quoted_list: bool = False,
) -> Any:
    """Specify an argument."""

    return ArgumentInfo(
        # Parameter
        default=default,
        # Arguments can only have one param declaration
        # it will be generated from the param name
        param_decls=None,
        type=type,
        callback=callback,
        metavar=metavar,
        expose_value=expose_value,
        is_eager=is_eager,
        envvar=envvar,
        shell_complete=shell_complete,
        # TyperArgument
        show_default=show_default,
        show_choices=show_choices,
        show_envvar=show_envvar,
        allow_from_autoenv=allow_from_autoenv,
        help=help,
        hidden=hidden,
        # Choice
        case_sensitive=case_sensitive,
        # Numbers
        min=min,
        max=max,
        clamp=clamp,
        # DateTime
        formats=formats,
        # File
        mode=mode,
        encoding=encoding,
        errors=errors,
        lazy=lazy,
        atomic=atomic,
        # Path
        exists=exists,
        file_okay=file_okay,
        dir_okay=dir_okay,
        writable=writable,
        readable=readable,
        resolve_path=resolve_path,
        allow_dash=allow_dash,
        path_type=path_type,
        # Shell-Quoted List
        shell_quoted_list=shell_quoted_list,
    )


def VersionOption(
    version: Optional[str] = None,
    *param_decls: str,
    package_name: Optional[str] = None,
    prog_name: Optional[str] = None,
    message: Optional[str] = None,
    # Option
    help: Optional[str] = "Show the version and exit.",
    hidden: bool = False,
    group: Optional[cloup.OptionGroup] = None,
) -> Any:
    """Specify a ``--version`` option which immediately prints the version number and exits the program.

    If ``version`` is not provided, Typer will try to detect it using :func:`importlib.metadata.version` to get the version for the ``package_name``.

    If ``package_name`` is not provided, Typer will try to detect it by inspecting the stack frames. This will be used to detect the version, so it must match the name of the installed package.

    :param version: The version number to show. If not provided, Typer will try to detect it.
    :param param_decls: One or more option names. Defaults to the single value ``"--version"``.
    :param package_name: The package name to detect the version from. If not provided, Typer will try to detect it.
    :param prog_name: The name of the CLI to show in the message. If not provided, it will be detected from the command.
    :param message: The message to show. The values ``%(prog)s``, ``%(package)s``, and ``%(version)s`` are available. Defaults to ``"%(prog)s, version %(version)s"``.

    :raise RuntimeError: ``version`` could not be detected.
    """

    if message is None:
        message = _("%(prog)s, version %(version)s")

    if version is None and package_name is None:
        frame = inspect.currentframe()
        f_back = frame.f_back if frame is not None else None
        f_globals = f_back.f_globals if f_back is not None else None
        # break reference cycle
        # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
        del frame

        if f_globals is not None:
            package_name = f_globals.get("__name__")

            if package_name == "__main__":
                package_name = f_globals.get("__package__")  # pragma: no cover

            if package_name:
                package_name = package_name.partition(".")[0]

    def callback(ctx: click.Context, param: click.Parameter, value: bool) -> None:
        if not value or ctx.resilient_parsing:
            return  # pragma: no cover

        nonlocal prog_name
        nonlocal version

        if prog_name is None:
            prog_name = ctx.find_root().info_name

        if version is None and package_name is not None:
            try:
                version = metadata.version(package_name)
            except metadata.PackageNotFoundError:
                raise RuntimeError(
                    f"{package_name!r} is not installed. Try passing 'package_name' instead."
                ) from None

        if version is None:
            raise RuntimeError(  # pragma: no cover
                f"Could not determine the version for {package_name!r} automatically."
            )

        click.echo(
            message % {"prog": prog_name, "package": package_name, "version": version},
            color=ctx.color,
        )
        ctx.exit()

    if not param_decls:
        param_decls = ("--version",)

    return OptionInfo(
        # Parameter
        param_decls=param_decls,
        callback=callback,
        expose_value=False,
        is_eager=True,
        envvar=None,
        # Option
        is_flag=True,
        allow_from_autoenv=False,
        help=help,
        hidden=hidden,
        group=group,
    )


def option_group(
    title: str,
    *options: str,
    help: Optional[str] = None,
    constraint: Optional[cloup.constraints.Constraint] = None,
    hidden: bool = False,
) -> Callable[[CommandFunctionType], CommandFunctionType]:
    """Specify an option group."""

    if not isinstance(title, str):
        raise TypeError(
            "the first argument of `@option_group` must be its title, a string; "
            "you probably forgot it"
        )

    if not options:
        raise ValueError("you must provide at least one option")

    def decorator(f: CommandFunctionType) -> CommandFunctionType:
        opt_group = cloup.OptionGroup(
            title, help=help, constraint=constraint, hidden=hidden
        )
        f_obj = cast(Any, f)
        if not hasattr(f, "__opt_groups"):
            f_obj.__opt_groups = []
        f_obj.__opt_groups.append((opt_group, options))
        return f

    return decorator


def constraint(
    constr: cloup.constraints.Constraint,
    *params: str,
) -> Callable[[CommandFunctionType], CommandFunctionType]:
    """Specify a parameter constraint."""

    return cloup.constraint(constr, params)
