import os
import builtins
import keyword

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from tabulate import tabulate
from pygments.lexers.python import PythonLexer
from pygments.lexers import PythonLexer


ERR = "\033[31m"
BS = "\033[0m"
YELLOW = "\033[33m"

script_dir = os.path.dirname(os.path.abspath(__file__))

class Data:

    grammatical = {
        **dict.fromkeys({name for name in dir(builtins) if name[0].islower()}),
        **dict.fromkeys(keyword.kwlist),
        **dict.fromkeys({e for e in dir(builtins) if "Error" in e or "Exception" in e})
    }
    last_error =          {}
    simple_base_command = {}
    repl_mode =           {}
    local_repl_mode =     {}
    _repl_cache_id =      0
    pyt_lex =             PythonLexer()
    color_container =     {}
    line_name_format =    ""
    script_file =         ""
    separator =           False
    color_2 =             False
    prompt =              ""
    settings =            {}
    shell_container =     {}
    pt_style =            {}
    script_dir =          ""

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

def PFT(text: str, data: Data) -> None:
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

def post(context: dict, data: Data) -> None:
    data.last_error = context
    PFT(f"{context["e"]}\npost_code: {context["code"]}\n{context["comment"]}", data)

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
        context = {
            "e": e,
            "code": 21.0,
            "comment": ""
        }
        post(context, data)
        result.append(str(value))

    # // macros beta
    value_copy = value.copy()
    index = 0
    for i in value_copy:
        if value_copy[index][:2] == ">#" and is_int_to_str(value_copy[index][2:]):
            goto_index = int(value_copy[index][2:])
            if len(command_arg) > (alias_position + goto_index):
                value_copy[index] = command_arg[alias_position + goto_index]
        elif value_copy[index][2:] == "!#" and is_int_to_str(value_copy[index][:2]):
            goto_index = int(value_copy[index][2:])
            if len(command_arg) > goto_index:
                value_copy[index] = command_arg[goto_index]
        elif value_copy[index] == "_#?_:":
            value_copy[index] = input("_#?_: ")
        index = index + 1
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
    filename = f"<simple_shell_repl_{data._repl_cache_id}>"
    data.line_cache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
    return filename