import os
import json
import shlex

from pyre_bottom_toolbar import bottom_toolbar
from pyre_alias import alias_parser
from pyre_core import (
    pft,
    post,
    command_separators,
    register_repl_source,
    buffer,
    Data,
    line_num,
    traceback_format,
    flag_mapping,
    reverse_search_flag
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
from pyre_const import (
    DEFAULT_SETTINGS,
    FILE_HISTORY,
    SETTINGS_FILE,
    NOP
)
from pyre_prompt_toolkit import completer
from pyre_bindings import bindings
from prompt_toolkit import PromptSession

#_________________________________________________________________________________________________

from prompt_toolkit.history import FileHistory
from pygments.token import string_to_tokentype
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.completion import DynamicCompleter
from prompt_toolkit.styles import style_from_pygments_dict

#_________________________________________________________________________________________________

def dispatcher(data: Data) -> None:
    data.postfix = " ".join(data.argv[1:])
    data.argc = len(data.argv)

    command_map = {
        "_pyt-eval_": pyt_eval,
        "_pyt-exec_": pyt_exec,
        "_pyt++_": pyt_pp,
        "_pyt_": pyt,
        "_._": shell_command,
        "_sh_": sh,
        "_?_": source_code,
        "_#_": NOP,
    }
    func = command_map.get(data.argv[0])
    if func:
         func(data)
         return
    if data.argv[0] in data.settings["plugin"]:
        load_plugin(data, data.argv[0])
        return
    e = f"[dispatcher]: unknown command: {data.argv[0]}"
    post(e, data)

#_________________________________________________________________________________________________

def pars_command(data: Data) -> None:
    if data.settings["shlex"]:
        try:
            data.argv = shlex.split(data.command, posix=bool(data.settings["posix"]))
        except ValueError as e:
            post(e, data)
            return None
    else:
        data.argv = data.command.split()

    if len(data.argv) < 1:
        e = "[pars_command]: not enough arguments"
        post(e, data)
        return None
    if data.settings["alias_globals"]:
        data.argv = alias_parser(data.settings["alias_dict"], data.argv, "global")
    if data.settings["separator"]:
        commands = command_separators(data.argv)
        for i in commands:
            if data.settings["alias_locals"]:
                data.argv = alias_parser(data.settings["alias_dict"], i, "local")
            dispatcher(data)
    else:
        if data.settings["alias_locals"]:
            i = alias_parser(data.settings["alias_dict"], data.argv, "local")
        else:
            i = data.argv
        data.argv = i
        dispatcher(data)

#_________________________________________________________________________________________________

def settings_load(data: Data, file: str = SETTINGS_FILE) -> None:
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
        data.repl_mode = data._local_repl_mode

    data.settings = settings

    try:
        pygments_token_dict = {
            string_to_tokentype(key): value
            for key, value in settings["color"].items()
        }
    except (ValueError, AttributeError) as e:
        pygments_token_dict = {}
        post(e, data)
    data.pt_style = style_from_pygments_dict(pygments_token_dict)

def initialisation() -> Data:
    data = Data()
    data.script_dir = os.path.dirname(os.path.abspath(__file__))
    settings_load(data)
    # noinspection PyTypeChecker
    data.api = {
        "settings_load": settings_load,
        "post": post,
        "pft": pft,
        "command_separators": command_separators,
        "pars_command": pars_command,
        "dispatcher": dispatcher,
        "buffer": buffer,
        "alias_parser": alias_parser,
        "data": data,
        "register_repl_source": register_repl_source,
        "hook_dispatch": hooks_dispatch,
        "traceback_format": traceback_format,
        "flag_mapping": flag_mapping,
        "reverse_search_flag": reverse_search_flag,
        "NOP": NOP
    }
    hooks_dispatch(data, "init", {"data": data})
    return data

#_________________________________________________________________________________________________

def repl_cycle(data: Data) -> None:
    toolbar = lambda: bottom_toolbar(data)
    session = PromptSession(
        history=FileHistory(FILE_HISTORY),
        include_default_pygments_style=False,
        key_bindings=bindings,
    )
    session.app.data = data
    session.app.mode = "repl_cycle"
    while True:
        try:
            data.command = session.prompt(
                data.settings["prompt"],
                completer=DynamicCompleter(lambda: completer(data)),
                multiline=data.settings["multiline"],
                lexer=PygmentsLexer(data.lexer),
                style=data.pt_style,
                prompt_continuation=lambda w, h, s: line_num(w, h, s, data.settings["line_name_format"]),
                vi_mode=data.settings["vi_mode"],
                mouse_support=data.settings["mouse_support"],
                bottom_toolbar=toolbar() if data.settings["bottom_toolbar"] else None,
            )
            pars_command(data)
        except (EOFError, KeyboardInterrupt):
            pass
        except Exception as e:
            post(e, data)
            return

def main() -> None:
    repl_cycle(initialisation())

if __name__ == "__main__":
    main()

#_________________________________________________________________________________________________
