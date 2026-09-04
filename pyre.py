"""
This is python repl
"""

#________________________________________________________________________________________________

import os
import json
import shlex
import linecache

#_________________________________________________________________________________________________

from pyre_core import (
    PFT,
    post,
    command_separators,
    register_repl_source,
    alias_parser,
    buffer,
    Data,
    line_num,
)
from pyre_commands import (
    sh,
    pyt,
    pyt_pp,
    pyt_eval,
    pyt_exec,
    source_code,
    shell_command
)
from pyre_plug_load import (
    load_plugin,
    hooks_dispatch
)
from pyre_prompt_toolkit import completer
from pyre_const import DEFAULT_SETTINGS
from pyre_bindings import bindings

#_________________________________________________________________________________________________

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from pygments.token import string_to_tokentype
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.completion import DynamicCompleter
from prompt_toolkit.styles import style_from_pygments_dict

#_________________________________________________________________________________________________

local_repl_mode = {}

def dispatcher(data: Data) -> None:
    data.command_prefix = " ".join(data.command_arg[1:])
    data.command_arg_int = len(data.command_arg)

    command_map = {
        "_pyt-eval_": pyt_eval,
        "_pyt-exec_": pyt_exec,
        "_pyt++_":    pyt_pp,
        "_pyt_":      pyt,
        "_._":        shell_command,
        "_sh_":       sh,
        "_?_":        source_code,
        "_#_":        lambda *args : None,
    }
    func = command_map.get(data.command_arg[0])
    if func:
        func(data)
    elif data.command_arg[0] in data.settings["plugin"]:
        load_plugin(data)
    else:
        e = f"[dispatcher]: unknown command: {data.command_arg[0]}"
        post(e, data)

#_________________________________________________________________________________________________

def pars_command(data: Data) -> None:
    if data.settings.get("shlex", False):
        try:
            data.command_arg = shlex.split(data.command, posix=bool(data.settings.get("posix", False)))
        except ValueError as e:
            post(e, data)
            return None
    else:
        data.command_arg = data.command.split()
    data.command_arg_int = len(data.command_arg)
    if data.command_arg_int < 1:
        e = "[pars_command]: not enough arguments"
        post(e, data)
        return None
    if data.settings.get("alias_globals", False):
        data.command_arg = alias_parser(data, data.settings.get("alias_dict", {}), data.command_arg, "global")
    if data.settings.get("separator"):
        commands = command_separators(data.command_arg)
        for i in commands:
            if data.settings.get("alias_locals", False):
                data.command_arg = alias_parser(data, data.settings.get("alias_dict", {}), i, "local")
            dispatcher(data)
    else:
        if data.settings.get("alias_locals", False):
            i = alias_parser(data, data.settings.get("alias_dict", {}), data.command_arg, "local")
        else:
            i = data.command_arg
        dispatcher(data)

#_________________________________________________________________________________________________

def settings_load(data: Data, file: str = ".pyre_settings.json") -> None:
    try:
        with open(file, encoding="utf-8") as f:
            settings = json.load(f)
    except Exception as e:
        post(e, data)
        settings = {}
    settings = {
        **DEFAULT_SETTINGS,
        **settings,
    }
    if settings["repl_mode"] == "globals":
        data.repl_mode = globals()
        data.repl_mode["data"] = data
    else:
        data.repl_mode = local_repl_mode

    data.settings         = settings

    try:
        pygments_token_dict = {
            string_to_tokentype(key): value
            for key, value in settings["color"].items()
        }
    except (ValueError, AttributeError) as e:
        pygments_token_dict = {
            string_to_tokentype(key): value
            for key, value in {}.items()
        }
        post(e, data)

    data.pt_style = style_from_pygments_dict(pygments_token_dict)
    data.script_dir = os.path.dirname(os.path.abspath(__file__))

def initialisation() -> Data:
    data = Data()
    data.line_cache = linecache
    settings_load(data)
    data.api = {
        "settings_load": settings_load,
        "post": post,
        "PFT": PFT,
        "command_separators": command_separators,
        "pars_command": pars_command,
        "dispatcher": dispatcher,
        "buffer": buffer,
        "alias_parser": alias_parser,
        "data": data,
        "register_repl_source": register_repl_source,
        "hook_dispatch": hooks_dispatch
    }
    hooks_dispatch(data, "init", {"data": data})
    return data

#_________________________________________________________________________________________________

def repl_cycle(data: Data) -> None:
    while True:
        try:
            data.command = prompt(
                data.settings.get("prompt", ">>> "),
                completer=DynamicCompleter(lambda: completer(data)),
                multiline=data.settings.get("multiline", False),
                lexer=PygmentsLexer(data.lexer),
                style=data.pt_style,
                prompt_continuation=lambda w, h, s: line_num(w, h, s, data.settings["line_name_format"]),
                history=FileHistory(".py_history"),
                include_default_pygments_style=False,
                key_bindings=bindings
                )
            pars_command(data)
        except (EOFError, KeyboardInterrupt):
            pass
        except Exception as e:
            post(e, data)
            return

def main() -> None:
    data = initialisation()
    repl_cycle(data)

if __name__ == "__main__":
    main()

#_________________________________________________________________________________________________
