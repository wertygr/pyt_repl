from __future__ import annotations
import sys
from types import TracebackType
from typing import TypedDict, Callable, Any, Protocol, TextIO
from prompt_toolkit.styles import BaseStyle
from pygments.lexer import RegexLexer

class Stringable(Protocol):
    def __str__(self) -> str:
        ...

class OptBuffer(Protocol):
    def __call__(self, mode: str, text: str = "") -> str|None:
        ...

class OptPost(Protocol):
    def __call__(self, e: TracebackType|BaseException|str, data: PluginData, use_hook: bool = True) -> None:
        ...

class OptPft(Protocol):
    def __call__(self, text: Stringable, data: PluginData, end: str= "\n", use_hook: bool = True, file:TextIO = sys.stdout) -> None:
        ...

class PluginApi(TypedDict):
    settings_load: Callable[[PluginData, str], None]
    post: OptPost
    pft: OptPft
    command_separators: Callable[[list[str]], list[list[str]]]
    pars_command: Callable[[PluginData], None]
    dispatcher: Callable[[PluginData], None]
    buffer: OptBuffer
    alias_parser: Callable[[PluginData, dict, list[str], str], list]
    data: PluginData
    register_repl_source: Callable[[PluginData, str], None]
    hook_dispatch: Callable[[PluginData, str, dict], list[Any]]
    traceback_format: Callable[[TracebackType|BaseException|str], str]
    flag_mapping: Callable[
        [dict[str, tuple[Callable[..., Any], bool]], list[str], Any, Any],
        None
    ]
    reverse_search_flag: Callable[[set[str], list[str], str], str]

class CommandContext(TypedDict):
    argv: list[str]
    postfix: str
    argc: int

class PluginData:
    last_error: str
    base_command: dict
    repl_mode: dict
    _repl_cache_id: int
    settings: dict
    script_dir: str
    repl_file: str
    pt_style: BaseStyle

    api: PluginApi

    plugin_space: dict
    pyt_plus_old_text: str

    command: str
    command_prefix: str
    command_arg_int: int
    command_arg: list[str]

    plugin_list: set[str]

    lexer: type[RegexLexer]
    lexer_instance: RegexLexer