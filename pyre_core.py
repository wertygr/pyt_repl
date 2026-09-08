#_________________________________________________________________________________________________

import traceback
import linecache
from collections import deque
from typing import Any, Callable
from types import TracebackType
from functools import wraps
from dataclasses import dataclass, field
from plugins.plugin_tools.plugin_types import (PluginApi)

#_________________________________________________________________________________________________

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import BaseStyle
from pygments.lexers.python import PythonLexer # type: ignore
from pygments.lexers import PythonLexer

from pyre_const import NO_OP

#_________________________________________________________________________________________________

@dataclass()
class Data:
    last_error =          ""
    repl_mode =           {}
    repl_cache_id =      0
    pyt_lex =             PythonLexer()
    settings =            {}
    pt_style: BaseStyle|None = field(default=None, init=False)
    script_dir =          ""

    api: PluginApi =      field(default_factory=dict) # type: ignore
    plugin_space =        {}
    _local_repl_mode =    {}

    pyt_plus_old_text =   ""

    command =             ""
    command_prefix =      ""
    command_arg_int =     0
    command_arg =         []

    lexer =               PythonLexer
    lexer_instance =      lexer()

#_________________________________________________________________________________________________

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
            if data.command_arg_int < min_args:
                post(f"[{func.__name__}]: not enough arguments", data)
                return None
            return func(data)
        return wrapper
    return decorator

def PFT(text: Any, data: Data, end: str= "\n") -> None:
    lexer = data.lexer_instance
    tokens = list(lexer.get_tokens(str(text)))
    print_formatted_text(
        PygmentsTokens(
            tokens
        ),
        style=data.pt_style,
        end=end
    )
    hooks_dispatch = data.api.get("hook_dispatch", NO_OP)
    hooks_dispatch(data, "PFT", {"text": f"{text}"}) # type: ignore

_buffer = ""
def buffer (mode: str = "copy", text: str = "") -> str|None:
    global _buffer
    if mode == "copy":
        return _buffer
    elif mode == "paste":
        _buffer = text
    elif mode == "add":
        _buffer += text

def traceback_format(e: TracebackType|BaseException|str) -> str:
    if isinstance(e, TracebackType):
        e = "".join(traceback.format_tb(e))
    elif isinstance(e, BaseException):
        e = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    return e

def post(e: Any, data: Data) -> None:
    e = traceback_format(e)
    data.last_error = e
    hooks_dispatch = data.api.get("hook_dispatch", NO_OP)
    hooks_dispatch(data, "post", {"err": f"{e}"}) # type: ignore
    PFT(e, data)

def command_separators(command_arg: list[str]) -> list[list[str]]:
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

def alias_position_validate(alias_position: int, alias_settings: dict) -> bool:
    position =  alias_settings.get("position", None)
    if position is None:
        return True
    if isinstance(position, list) and alias_position in position:
        return True
    return False

def alias_paste(value: list[str], result: list[str], token: str, command_arg: list[str], alias_position: int, data: Data) -> list[str]:
    if not(isinstance(value, list)):
        e = f"Invalid value type {type(value)} for alias {token}"
        post(e, data)
        result.append(str(value))
    # // macros beta
    value_copy = value.copy()
    for index, i in enumerate(value_copy):
        if value_copy[index][:2] == ">#" and str_is_int(value_copy[index][2:]):
            goto_index = int(value_copy[index][2:])
            if len(command_arg) > (alias_position + goto_index):
                value_copy[index] = command_arg[alias_position + goto_index]
        elif value_copy[index][:2] == "!#" and str_is_int(value_copy[index][2:]):
            goto_index = int(value_copy[index][2:])
            if len(command_arg) > goto_index:
                value_copy[index] = command_arg[goto_index]
        elif value_copy[index] == "_#?_:":
            value_copy[index] = input("_#?_: ")
    result.extend(value_copy)
    return result

def alias_parser(data: Data, alias_dict: dict, command_arg: list, mode: str) -> list[str]:
    result = []
    for index, item in enumerate(command_arg):
        if not(item in alias_dict):
            result.append(item)
            continue

        item_dict = alias_dict.get(item, {})
        # __ __ __ __ __ __ __ __
        value = item_dict.get("value", "NONE_ALIAS")
        scope = item_dict.get("scope", "local")
        # __ __ __ __ __ __ __ __
        if (scope == mode) and (alias_position_validate(index, alias_dict[item])):
            result = alias_paste(value, result, item, command_arg, index, data)
        else:
            result.append(item)
    return result

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
    data.repl_cache_id += 1
    filename = f"<py_repl_{data.repl_cache_id}>"
    linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
    return filename