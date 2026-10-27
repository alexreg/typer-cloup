import inspect
import io
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

import click
import cloup

if TYPE_CHECKING:  # pragma: no cover
    import click.shell_completion
    from cloup.constraints import BoundConstraintSpec

    from .core import TyperCommand, TyperGroup
    from .main import Typer  # noqa


NoneType = type(None)

AnyType = Type[Any]

Required = ...


class Context(cloup.Context):
    def __init__(
        self,
        # click.Context
        command: "click.Command",
        parent: Optional["click.Context"] = None,
        info_name: Optional[str] = None,
        obj: Optional[Any] = None,
        auto_envvar_prefix: Optional[str] = None,
        default_map: Optional[Dict[str, Any]] = None,
        terminal_width: Optional[int] = None,
        max_content_width: Optional[int] = None,
        resilient_parsing: bool = False,
        allow_extra_args: Optional[bool] = None,
        allow_interspersed_args: Optional[bool] = None,
        ignore_unknown_options: Optional[bool] = None,
        help_option_names: Optional[List[str]] = None,
        token_normalize_func: Optional[Callable[[str], str]] = None,
        color: Optional[bool] = None,
        show_default: Optional[bool] = None,
        # cloup.Context
        align_option_groups: Optional[bool] = None,
        align_sections: Optional[bool] = None,
        show_subcommand_aliases: Optional[bool] = None,
        show_constraints: Optional[bool] = None,
        check_constraints_consistency: Optional[bool] = None,
        formatter_settings: Dict[str, Any] = {},
    ):
        if auto_envvar_prefix is None:
            if (
                parent is not None
                and parent.auto_envvar_prefix is not None
                and info_name is not None
            ):
                auto_envvar_prefix = info_name.upper()
                if parent.auto_envvar_prefix:
                    auto_envvar_prefix = (
                        f"{parent.auto_envvar_prefix}_{auto_envvar_prefix}"
                    )

        super().__init__(
            command=command,
            parent=parent,
            info_name=info_name,
            obj=obj,
            auto_envvar_prefix=auto_envvar_prefix,
            default_map=default_map,
            terminal_width=terminal_width,
            max_content_width=max_content_width,
            resilient_parsing=resilient_parsing,
            allow_extra_args=allow_extra_args,
            allow_interspersed_args=allow_interspersed_args,
            ignore_unknown_options=ignore_unknown_options,
            help_option_names=help_option_names,
            token_normalize_func=token_normalize_func,
            color=color,
            show_default=show_default,
            align_option_groups=align_option_groups,
            align_sections=align_sections,
            show_subcommand_aliases=show_subcommand_aliases,
            show_constraints=show_constraints,
            check_constraints_consistency=check_constraints_consistency,
            formatter_settings=formatter_settings,
        )


class FileText(io.TextIOWrapper):
    pass


class FileTextWrite(FileText):
    pass


class FileBinaryRead(io.BufferedReader):
    pass


class FileBinaryWrite(io.BufferedWriter):
    pass


class CallbackParam(click.Parameter):
    pass


class DefaultPlaceholder:
    """
    You shouldn't use this class directly.

    It's used internally to recognize when a default value has been overwritten, even
    if the new value is `None`.
    """

    def __init__(self, value: Any):
        self.value = value

    def __bool__(self) -> bool:
        return bool(self.value)


DefaultType = TypeVar("DefaultType")

CommandFunctionType = TypeVar("CommandFunctionType", bound=Callable[..., Any])


def Default(value: DefaultType) -> DefaultType:
    """
    You shouldn't use this function directly.

    It's used internally to recognize when a default value has been overwritten, even
    if the new value is `None`.
    """
    return DefaultPlaceholder(value)  # type: ignore


class CommandInfo:
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type["TyperCommand"]] = None,
        context_settings: Optional[Dict[Any, Any]] = None,
        callback: Optional[Callable[..., Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
        section: Optional[cloup.Section] = None,
        constraints: Sequence["BoundConstraintSpec"] = (),
        show_constraints: Optional[bool] = None,
        align_option_groups: Optional[bool] = None,
        aliases: Optional[Iterable[str]] = None,
        formatter_settings: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.cls = cls
        self.context_settings = context_settings
        self.callback = callback
        self.help = help
        self.epilog = epilog
        self.short_help = short_help
        self.options_metavar = options_metavar
        self.add_help_option = add_help_option
        self.no_args_is_help = no_args_is_help
        self.hidden = hidden
        self.deprecated = deprecated
        self.section = section
        self.constraints = constraints
        self.show_constraints = show_constraints
        self.align_option_groups = align_option_groups
        self.aliases = aliases
        self.formatter_settings = formatter_settings


class TyperInfo:
    def __init__(
        self,
        typer_instance: Optional["Typer"] = Default(None),
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type["TyperGroup"]] = Default(None),
        invoke_without_command: bool = Default(False),
        no_args_is_help: bool = Default(False),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        section: Optional[cloup.Section] = Default(None),
        align_sections: Optional[bool] = Default(None),
        show_subcommand_aliases: Optional[bool] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        callback: Optional[Callable[..., Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        constraints: Sequence["BoundConstraintSpec"] = Default(()),
        show_constraints: Optional[bool] = Default(None),
        align_option_groups: Optional[bool] = Default(None),
        aliases: Optional[Iterable[str]] = Default(None),
        formatter_settings: Optional[Dict[str, Any]] = Default(None),
    ):
        self.typer_instance = typer_instance
        self.name = name
        self.cls = cls
        self.invoke_without_command = invoke_without_command
        self.no_args_is_help = no_args_is_help
        self.subcommand_metavar = subcommand_metavar
        self.chain = chain
        self.result_callback = result_callback
        self.section = section
        self.align_sections = align_sections
        self.show_subcommand_aliases = show_subcommand_aliases
        self.context_settings = context_settings
        self.callback = callback
        self.help = help
        self.epilog = epilog
        self.short_help = short_help
        self.options_metavar = options_metavar
        self.add_help_option = add_help_option
        self.hidden = hidden
        self.deprecated = deprecated
        self.constraints = constraints
        self.show_constraints = show_constraints
        self.align_option_groups = align_option_groups
        self.aliases = aliases
        self.formatter_settings = formatter_settings


class ParameterInfo:
    def __init__(
        self,
        *,
        default: Optional[Any] = None,
        param_decls: Optional[Sequence[str]] = None,
        type: Optional[Union[click.types.ParamType, Any]] = None,
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
    ):
        self.default = default
        self.param_decls = param_decls
        self.type = type
        self.callback = callback
        self.metavar = metavar
        self.expose_value = expose_value
        self.is_eager = is_eager
        self.envvar = envvar
        self.shell_complete = shell_complete
        # TyperArgument
        self.show_default = show_default
        self.show_choices = show_choices
        self.show_envvar = show_envvar
        self.allow_from_autoenv = allow_from_autoenv
        self.help = help
        self.hidden = hidden
        # Choice
        self.case_sensitive = case_sensitive
        # Numbers
        self.min = min
        self.max = max
        self.clamp = clamp
        # DateTime
        self.formats = formats
        # File
        self.mode = mode
        self.encoding = encoding
        self.errors = errors
        self.lazy = lazy
        self.atomic = atomic
        # Path
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.writable = writable
        self.readable = readable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash
        self.path_type = path_type
        # Shell-Quoted List
        self.shell_quoted_list = shell_quoted_list


class OptionInfo(ParameterInfo):
    def __init__(
        self,
        *,
        # ParameterInfo
        default: Optional[Any] = None,
        param_decls: Optional[Sequence[str]] = None,
        type: Optional[Union[click.types.ParamType, Any]] = None,
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
    ):
        super().__init__(
            default=default,
            param_decls=param_decls,
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
        self.prompt = prompt
        self.confirmation_prompt = confirmation_prompt
        self.prompt_required = prompt_required
        self.hide_input = hide_input
        self.is_flag = is_flag
        self.flag_value = flag_value
        self.count = count
        self.group = group


class ArgumentInfo(ParameterInfo):
    def __init__(
        self,
        *,
        # ParameterInfo
        default: Optional[Any] = None,
        param_decls: Optional[Sequence[str]] = None,
        type: Optional[Union[click.types.ParamType, Any]] = None,
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
    ):
        super().__init__(
            default=default,
            param_decls=param_decls,
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


class ParamMeta:
    empty = inspect.Parameter.empty

    def __init__(
        self,
        *,
        name: str,
        default: Any = inspect.Parameter.empty,
        annotation: Any = inspect.Parameter.empty,
    ) -> None:
        self.name = name
        self.default = default
        self.annotation = annotation
