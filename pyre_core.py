import json
import os
import builtins
import keyword
from typing import Any

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import style_from_pygments_dict
from pygments.token import string_to_tokentype
from tabulate import tabulate
from pygments.lexers.python import PythonLexer
from pygments.lexers import PythonLexer

script_dir = os.path.dirname(os.path.abspath(__file__))

BS = "\033[0m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"

class Data:

    grammatical = {
        **dict.fromkeys({name for name in dir(builtins) if name[0].islower()}),
        **dict.fromkeys(keyword.kwlist),
        **dict.fromkeys({e for e in dir(builtins) if "Error" in e or "Exception" in e})
    }
    last_error =          ""
    simple_base_command = {}
    repl_mode =           {}
    local_repl_mode =     {}
    _repl_cache_id =      0
    pyt_lex =             PythonLexer()
    color_container =     {}
    line_name_format =    ""
    script_file =         ""
    separator =           False
    prompt =              ""
    settings =            {}
    shell_container =     {}
    pt_style =            {}
    script_dir =          ""
    repl_file =           ""

    ss_api =              {}

    plugin_space =        {}

    command =             ""
    pyt_plus_old_text =   ""

    command_prefix =      ""
    command_arg_int =     0
    command_arg =         []

    line_cache =          []

    lexer =               PythonLexer
    lexer_instance =      lexer()
    session =             None

def PFT(text: str,data: Data) -> None:
    lexer = data.lexer_instance
    tokens = list(lexer.get_tokens(str(text)))
    print_formatted_text(
        PygmentsTokens(
            tokens
        ),
        style=data.pt_style
    )
_buffer = ""
def buffer (mode: str = "copy", text: str = ""):
    global _buffer
    if mode == "copy":
        return _buffer
    if mode == "paste":
        _buffer = text
    elif mode == "add":
        _buffer += text

def post(e: Any, data: Data) -> None:
    data.last_error = e
    PFT(f"{e}", data)

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

def alias_parser(data: Data, alias_dict: dict, command_arg: list, mode: str) -> list: # V5.1
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

def alias_list(data) -> None:
    alias_dict = data.settings
    table_data = []

    for i in alias_dict.get("alias_dict", {}):
        alias_info = alias_dict["alias_dict"][i]

        scope = alias_info.get("scope", "local")
        value = alias_info.get("value", "NONE_ALIAS")
        position = alias_info.get("position", None)

        table_data.append([i, scope, position, value])

    headers = ["alias", "scope", "position", "value"]

    PFT(tabulate(table_data, headers=headers, tablefmt="grid"), data)

def dynamics_completer(data: Data):
    return {
        **dict.fromkeys(data.repl_mode, None),
        **data.grammatical
    }

def line_num(
        width: int,
        line_number: int,
        is_soft_wrap: int,
        data: Data
    ) -> str:
    return data.line_name_format.format(
         width=width,
         line_number=line_number + 1,
         is_soft_wrap=is_soft_wrap
    )

def register_repl_source(source: str, data) -> str:
    data._repl_cache_id += 1
    filename = f"<py_repl_{data._repl_cache_id}>"
    data.line_cache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
    return filename


def settings_load(data: Data, file: str = ".pyre_settings.json") -> None:
    try:
        with open(file, encoding="utf-8") as f:
            settings = json.load(f)
    except Exception as e:
        post(e, data)
        settings = {}

    line_name_format =    settings.get("line_name_format", "{line_number} |")
    script_file =         settings.get("file", {}).get("script_file", None)

    if isinstance(script_file, str):
        script_file = script_file
    else:
        script_file = None

    data.separator =      settings.get("separator", False)

    data.prompt =         settings.get("prompt", ">>> ")

    if settings.get("repl_mode", "locals") == "globals":
        data.repl_mode = globals()
        data.repl_mode["data"] = data
    else:
        data.repl_mode = data.local_repl_mode

    if settings.get("shell_container", False):
        data.shell_container = data.repl_mode
    else:
        data.shell_container = {}

    data.script_file      = script_file
    data.line_name_format = line_name_format
    data.settings         = settings

    pygments_token_dict = {
        string_to_tokentype(key): value
        for key, value in settings.get("color", {}).items()
    }
    data.pt_style =        style_from_pygments_dict(pygments_token_dict)
    data.script_dir =      os.path.dirname(os.path.abspath(__file__))