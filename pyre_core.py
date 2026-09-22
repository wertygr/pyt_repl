import sys
import traceback
import linecache
from collections import deque
from typing import Any, Callable, TextIO
from types import TracebackType
from functools import wraps
from plugins.plugin_tools.plugin_types import (PluginApi)

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import BaseStyle
from pygments.lexers import PythonLexer

from pyre_const import NOP

class Data:
    def __init__(self) -> None:
        self.last_error: str = ""
        self.repl_mode: dict = {}
        self._repl_cache_id: int = 0
        self.settings: dict = {}
        self.pt_style: BaseStyle # type: ignore
        self.script_dir: str = ""
        self.api: PluginApi = {} # type: ignore
        self.plugin_space: dict = {}
        self._local_repl_mode:dict = {}
        self._pyt_plus_old_text: str = ""
        self.command: str = ""
        self.postfix: str = ""
        self.argc: int = 0
        self.argv: list[str] = []
        self.lexer = PythonLexer
        self.lexer_instance = self.lexer()
        self.plugin_list: set[str] = set()

def reverse_search_flag(modes: set[str], flags: list[str], def_mode: str)-> str:
    for i in reversed(flags):
        if i in modes:
            return i
    return def_mode

def flag_mapping(flag_map: dict[str, tuple[Callable, bool]], command_args: list[str], *args, **kwargs) -> None:
    args_set = set(command_args)
    deque(
        (action(*args, **kwargs) for flag, (action, run_if_present) in flag_map.items()
         if (flag in args_set) == run_if_present),
        maxlen=0
    )

def require_args(min_args) -> Callable[[Callable], Callable]:
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(data) -> Any:
            if data.argc < min_args:
                post(f"[{func.__name__}]: not enough arguments(min argc: {min_args})", data)
                return None
            return func(data)
        return wrapper
    return decorator

def pft(text: Any, data: Data, end: str= "\n", use_hook: bool = True, file:TextIO = sys.stdout) -> None:
    lexer = data.lexer_instance
    tokens = list(lexer.get_tokens(str(text)))
    print_formatted_text(
        PygmentsTokens(
            tokens
        ),
        style=getattr(data, 'pt_style', None),
        end=end,
        include_default_pygments_style=False,
        file=file,
    )
    if use_hook:
        hooks_dispatch = data.api.get("hook_dispatch", NOP)
        hooks_dispatch(data, "pft", {"text": f"{text}"}) # type: ignore

def buffer (mode: str = "read", text: str = "") -> str|None:
    if not hasattr(buffer, "text"):
        buffer.text = ""
    if mode == "read":
        return buffer.text
    elif mode == "write":
        buffer.text = text
    elif mode == "write_add":
        buffer.text += text

def traceback_format(e: TracebackType|BaseException|str) -> str:
    if isinstance(e, TracebackType):
        e = "".join(traceback.format_tb(e))
    elif isinstance(e, BaseException):
        e = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    return e

def post(e: TracebackType|BaseException|str, data: Data, use_hook: bool = True) -> None:
    e = traceback_format(e)
    data.last_error = e
    if use_hook:
        hooks_dispatch = data.api.get("hook_dispatch", NOP)
        hooks_dispatch(data, "post", {"err": str(e)}) # type: ignore
    pft(e, data, use_hook=use_hook)

def command_separators(command_arg: list[str], token: str = "_&_") -> list[list[str]]:
    subarrays = []
    current = []
    for item in command_arg:
        if item == "_&_":
            if current:
                subarrays.append(current)
                current = []
        else:
            current.append(item)

    if current:
        subarrays.append(current)
    return subarrays

def str_is_int(string: str) -> bool:
    if not string:
        return False
    if string[0] in ["+","-"]:
        return string[1:].isdigit()
    return string.isdigit()

def line_num(
        width: int,
        line_number: int,
        is_soft_wrap: int,
        format_sample: str = "{line_number} |"
    ) -> str:
    return format_sample.format(
         width=width,
         line_number=line_number + 1,
         is_soft_wrap=is_soft_wrap
    )

def register_repl_source(source: str, data: Data) -> str:
    data._repl_cache_id += 1
    filename = f"<py_repl_{data._repl_cache_id}>"
    linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
    return filename