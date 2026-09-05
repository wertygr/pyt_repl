from __future__ import annotations
from typing import TypedDict, Callable, Any, Protocol

from prompt_toolkit.styles import BaseStyle

class OptBuffer(Protocol):
    def __call__(self, mode: str = ..., text: str = ...) -> str|None:
        ...

class PluginApi(TypedDict):
    settings_load: Callable[[PluginData, str], None]
    post: Callable[[Any, PluginData], None]
    PFT: Callable[[Any, PluginData], None]
    command_separators: Callable[[list[str]], list[list[str]]]
    pars_command: Callable[[PluginData], None]
    dispatcher: Callable[[PluginData], None]
    buffer: OptBuffer
    alias_parser: Callable[[PluginData, dict, list[str], str], list]
    data: PluginData
    register_repl_source: Callable[[PluginData, str], None]
    hook_dispatch: Callable[[PluginData, str, dict], list[Any]]

class CommandContext(TypedDict):
    command_arg: list[str]
    command_prefix: str
    command_arg_int: int

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