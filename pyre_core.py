#_________________________________________________________________________________________________

import traceback
from typing import Any
from types import TracebackType
from functools import wraps

#_________________________________________________________________________________________________

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import BaseStyle
from pygments.lexers.python import PythonLexer
from pygments.lexers import PythonLexer

#_________________________________________________________________________________________________

RESET = "\033[0m"
YELLOW = "\033[33m"

#_________________________________________________________________________________________________

class Data:

    last_error =          ""
    repl_mode =           {}
    _repl_cache_id =      0
    pyt_lex =             PythonLexer()
    settings =            {}
    pt_style: BaseStyle
    script_dir =          ""

    api =                 {}

    plugin_space =        {}

    pyt_plus_old_text =   ""

    command =             ""
    command_prefix =      ""
    command_arg_int =     0
    command_arg =         []

    line_cache =          []

    lexer =               PythonLexer
    lexer_instance =      lexer()

#_________________________________________________________________________________________________

def require_args(min_args):
    def decorator(func):
        @wraps(func)
        def wrapper(data):
            if data.command_arg_int < min_args:
                post(f"[{func.__name__}]: not enough arguments", data)
                return
            return func(data)

        return wrapper

    return decorator

def PFT(text: str, data: Data, end: str= "\n") -> None:
    lexer = data.lexer_instance
    tokens = list(lexer.get_tokens(str(text)))
    print_formatted_text(
        PygmentsTokens(
            tokens
        ),
        style=data.pt_style,
        end=end
    )
    hooks_dispatch = data.api.get("hook_dispatch", lambda *_: None)
    hooks_dispatch(data, "PFT", {"text": f"{text}"})

_buffer = ""
def buffer (mode: str = "copy", text: str = "") -> str|None:
    global _buffer
    if mode == "copy":
        return _buffer
    elif mode == "paste":
        _buffer = text
    elif mode == "add":
        _buffer += text

def post(e: Any, data: Data) -> None:
    if isinstance(e, TracebackType):
        e = "".join(traceback.format_tb(e))
    elif isinstance(e, BaseException):
        e = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    data.last_error = e
    hooks_dispatch = data.api.get("hook_dispatch", lambda *_: None)
    hooks_dispatch(data, "post", {"err": f"{e}"})
    PFT(e, data)

def command_separators(command_arg) -> list:
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

def is_int_to_str(string):
    if not string:
        return False
    if string[0] in ["+","-"]:
        return string[1:].isdigit()
    return string.lstrip('+-').isdigit()

def alias_position_validate(alias_position: int, alias_settings: dict) -> bool:
    position =  alias_settings.get("position", None)
    if position == None:
        return True
    if isinstance(position, list) and alias_position in position:
        return True
    return False

def alias_paste(value: list[str], result: list, token: str, command_arg: list[str], alias_position: int, data: Data) -> list:
    if not(isinstance(value, list)):
        e = f"Invalid value type {type(value)} for alias {token}"
        post(e, data)
        result.append(str(value))
    # // macros beta
    value_copy = value.copy()
    for index, i in enumerate(value_copy):
        if value_copy[index][:2] == ">#" and is_int_to_str(value_copy[index][2:]):
            goto_index = int(value_copy[index][2:])
            if len(command_arg) > (alias_position + goto_index):
                value_copy[index] = command_arg[alias_position + goto_index]
        elif value_copy[index][:2] == "!#" and is_int_to_str(value_copy[index][2:]):
            goto_index = int(value_copy[index][2:])
            if len(command_arg) > goto_index:
                value_copy[index] = command_arg[goto_index]
        elif value_copy[index] == "_#?_:":
            value_copy[index] = input("_#?_: ")
    result.extend(value_copy)
    return result

def alias_parser(data: Data, alias_dict: dict, command_arg: list, mode: str) -> list:
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

def register_repl_source(source: str, data) -> str:
    data._repl_cache_id += 1
    filename = f"<py_repl_{data._repl_cache_id}>"
    data.line_cache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
    return filename