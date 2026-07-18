import inspect
import types
import pprint
import os
import sys
import subprocess
import linecache

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import Style as PtStyle
from tabulate import tabulate

from simple_shell_lexer import PytLexer

# from tabulate import tabulate

ERR = "\033[31m"
BS = "\033[0m"
YELLOW = "\033[33m"

pyt_lex = PytLexer()

script_dir = os.path.dirname(os.path.abspath(__file__))



def make_ss_style(color_container):
    return PtStyle.from_dict(
        {
            'pygments.name.prefix':     color_container["prefix"],
            'pygments.literal.string':  color_container["string"],
            'pygments.literal.number':  color_container["number"],
            'pygments.keyword':         color_container["keyword"],
            'pygments.comment':         color_container["comment"],
            'pygments.name':            color_container["name"],
            'pygments.operator':        color_container["operator"],
            'pygments.punctuation':     color_container["punctuation"],
            'pygments.text':            color_container["text"],
            'pygments.name.defer':      color_container["def_name"],
            'pygments.name.error':      color_container["error"],
            'pygments.name.action':     color_container["action"],
        }
    )
color_container = {'prefix': '#C77DBB', 'string': '#6AAB73', 'number': '#2AACB8', 'keyword': 'bold #CF8E6D', 'comment': 'italic #7A7E85', 'name': '#BCBEC4', 'operator': '#cccccc', 'punctuation': '#ffffff', 'text': '#cccccc', 'def_name': '#56A8F5', 'error': 'underline #D64D5B', 'action': '#8888C6'}

_repl_cache_id = 0
def register_repl_source(source: str) -> str:
    global _repl_cache_id
    _repl_cache_id += 1
    filename = f"<simple_shell_repl_{_repl_cache_id}>"
    linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
    return filename

def PFT(text: str, ss_style=make_ss_style(color_container), lexer = pyt_lex) -> None:

    if isinstance(text, (dict, list, set)):
        text = pprint.pformat(text, indent=4, width=40, sort_dicts=False)

    tokens = list(lexer.get_tokens(str(text)))
    print_formatted_text(
        PygmentsTokens(
            tokens
        ),
        style=ss_style
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

def post (e = "", code = None, comment = "") -> None:
    PFT(f"{e}\npost_code: {code}\n{comment}")


def source_code(args_1, command_arg_int, command_arg, repl_mode, ss_style) -> None:
    _copy = ""
    text = ""

    if command_arg_int < 2:
        e = "[source_code]: not enough arguments"
        post(e, 14.0)
        return
    obj = repl_mode.get(command_arg[1])

    if callable(obj) or inspect.isclass(obj):
        try:
            _copy = inspect.getsource(obj)
            text = _copy
        except (OSError, TypeError):
            _copy = getattr(obj, "__doc__", "no docstring")
            text = f"{YELLOW}[no docstring]{BS}"
    elif isinstance(obj, types.ModuleType):
        try:
            _copy = inspect.getsource(obj)
            text = _copy
        except (OSError, TypeError):
            _copy = getattr(obj, "__doc__", "no docstring")
            text = f"{YELLOW}[no docstring]{BS}"
    elif command_arg[1] in repl_mode:
        _copy = repr(obj)
        text = f"{command_arg[1]} = {_copy}"
    else:
        text = f"[no object]: {command_arg[1]}"

    flag_map = {
        "-copy": [lambda: buffer("paste", text), True],
        "-silent": [lambda: PFT(text, ss_style), False],
    }
    for flag, (action, run_if_present) in flag_map.items():
        is_present = flag in command_arg[1:]

        if is_present == run_if_present:
            action()

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


def get_index(lst, index, mode = "normal"):
    if mode == "normal":
        try:
            return lst[index]
        except IndexError:
            return None
    else:
        try:
            test = lst[index]
            return True
        except IndexError:
            return False


def line_num(
        width=0,
        line_number=0,
        is_soft_wrap=0,
        line_name_format="{line_number:>{width}} |"
    ) -> str:
    return line_name_format.format(
        width=width,
        line_number=line_number,
        is_soft_wrap=is_soft_wrap
    )


def is_int_to_str(string):
    if not string:
        return False
    if string[0] in ["+","-"]:
        return string[1:].isdigit()
    return string.lstrip('+-').isdigit()

def alias_paste(value: list[str], result: list, token: str="__NONE_TOKEN__", command_arg: list = [], alias_position: int = 0) -> list:
    if not(isinstance(value, list)):
        e = f"Invalid value type {type(value)} for alias {token}"
        post(e, 21.0)
        result.append(str(value))

    # // macros beta
    index = 0
    for i in value:
        if value[index][:2] == ">#" and is_int_to_str(value[index][2:]):
            goto_index = int(value[index][2:])
            if len(command_arg) > (alias_position + goto_index):
                value[index] = command_arg[alias_position + goto_index]
        elif value[index][:2] == "!#" and is_int_to_str(value[index][:2]):
            goto_index = int(value[index][2:])
            if len(command_arg) > goto_index:
                value[index] = command_arg[goto_index]
        elif value[index] == "_#?_:":
            value[index] = input("_#?_: ")
        index = index + 1
    result.extend(value)
    return result


def global_alias(alias_dict: dict, command_arg: list) -> list: # V4 working
    result = []
    index = 0
    for item in command_arg:
        if item in alias_dict:
            item_dict = alias_dict.get(item, {})
            # __ __ __ __ __ __ __ __
            value = item_dict.get("value", "NONE_ALIAS")
            scope = item_dict.get("scope", "local")
            # __ __ __ __ __ __ __ __
            if scope == "global":
                result = alias_paste(value, result, item, command_arg, index)
            else:
                result.append(item)
        else:
            result.append(item)
        index = index + 1
    return result


def local_alias(alias_dict: dict, command_arg: list) -> list:
    result = []
    index = 0
    for item in command_arg:
        if item in alias_dict:
            item_dict = alias_dict.get(item, {})
            # __ __ __ __ __ __ __ __
            value = item_dict.get("value", "NONE_ALIAS")
            scope = item_dict.get("scope", "local")
            position = item_dict.get("position", 0)
            # __ __ __ __ __ __ __ __
            if isinstance(position, int):
                if (len(command_arg) > position) and (item == command_arg[position]):
                    result = alias_paste(value, result, item, command_arg, index)
                else:
                    result.append(item)
            elif (position == None) and (scope == "local"):
                result = alias_paste(value, result, item, command_arg, index)
            else:
                post()
                result.append(item)
        else:
            result.append(item)
        index = index + 1
    return result


def alias_list(alias_dict: dict) -> None:
    table_data = []

    for i in alias_dict.get("alias_dict", {}):
        alias_info = alias_dict["alias_dict"][i]

        scope = alias_info.get("scope", "local")
        value = alias_info.get("value", "NONE_ALIAS")

        if scope == "local":
            position = alias_info.get("position", 0)
        else:
            position = "---"

        table_data.append([i, scope, position, value])

    headers = ["alias", "scope", "position", "value"]

    PFT(tabulate(table_data, headers=headers, tablefmt="grid"))


def fallback_script_run(file, command_arg) -> None:
    script_file = file.get("script_file", None).format(script_dir=script_dir)
    mode = file.get("mode", 0)

    if mode == 1:
        fallback_command = []
        fallback_command.append(" ".join(command_arg))
        # print(fallback_command)
    else:
        fallback_command = command_arg

    if script_file != None:
        try:
            subprocess.run([sys.executable, script_file, *fallback_command])
        except Exception as e:
            post(e, 20.1)
    else:
        post(f"command not found: {command_arg}", 20.0)

def is_posix(settings: dict) -> bool:
    posix_flag = settings.get("posix", False)
    if not(posix_flag in ["auto", True, False, None]):
        posix_flag = False
        post(f"invalid settings(incorrect type - {type(settings.get("posix", False))}): \"posix\": {settings['posix']}", 21.0)
    if posix_flag in [None, "auto"]: # auto mode
        if os.name == "nt":
            return False
        elif os.name == "posix":
            return True
        elif os.name == "darwin":
            return True
        return True
    else:
        return posix_flag
