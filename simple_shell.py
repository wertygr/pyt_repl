"""
This is python repl
"""
#________________________________________________________________________________________________

import shlex
import linecache
from pathlib import Path

#_________________________________________________________________________________________________

from simple_shell_core import PFT
from simple_shell_core import post
from simple_shell_core import command_separators
from simple_shell_core import alias_parser
from simple_shell_core import buffer
from simple_shell_core import Data
from simple_shell_core import line_num
from simple_shell_core import register_repl_source
from simple_shell_core import settings_load
from simple_shell_commands import source_code
from simple_shell_commands import pyt_eval
from simple_shell_commands import sh
from simple_shell_commands import pyt
from simple_shell_commands import pyt_exec
from simple_shell_commands import pyt_pp
from simple_shell_commands import shell_command
from simple_shell_plug_loader import plugin_ss
from simple_shell_prompt_toolkit import completer
#_________________________________________________________________________________________________

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import DynamicCompleter

#_________________________________________________________________________________________________

def plugin_load(data: Data) -> bool:
    if not(data.command_arg[0] in data.settings.get("plugin", {})):
        return False
    plugin_ss(data)
    return True

#_________________________________________________________________________________________________

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
    elif plugin_load(data):
        pass
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
    if data.separator:
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

def initialisation() -> Data:
    data = Data()
    data.repl_file = Path(__file__).resolve()
    data.line_cache = linecache
    settings_load(data)
    data.simple_base_command = {
        "_#_": None,
        "_pyt_": data.grammatical,
        "_pyt-exec_": data.grammatical,
        "_pyt-eval_": data.grammatical,
        "_&_": None,
        "_?_": None,
        "_._": {
            "exit": None,
            "clear": None,
            "history_del": None,
            "settings_reload": None,
            "plugins_list": None,
            "run": {
                "{script_dir}": None
            },
            "help": None,
            "list_vf": None,
            "read_vf": dict.fromkeys(linecache.cache, None),
            "rname_vf": None
        },
        "_pyt++_": {
            "old": None
        },
        "_sh_": None,

        **dict.fromkeys(data.settings.get("plugin", {}), None),
        **dict.fromkeys(data.settings.get("alias_dict", {}), None),
    }
    data.ss_api = {
        "color_container": data.color_container,

        "settings": data.settings,
        "prompt": data.prompt,

        "script_dir": data.script_dir,
        "script_file": data.script_file,

        "pyt_lex": data.pyt_lex,
        "pt_style": data.pt_style,

        "post": post,
        "PFT": PFT,
        "command_separators": command_separators,
        "pars_command": pars_command,
        "dispatcher": dispatcher,
        "buffer": buffer,
        "alias_parser": alias_parser,
        "data": data,
        "register_repl_source": register_repl_source
    }

    data.session = PromptSession(
        completer=DynamicCompleter(lambda: completer(data)),
        multiline=data.settings.get("multiline", False),
        lexer=PygmentsLexer(data.lexer),
        style=data.pt_style,
        prompt_continuation=lambda w, h, s: line_num(w, h, s, data),
        history=FileHistory(".ss_history"),
        include_default_pygments_style=False
    )

    return data

def repl_cycle(data: Data) -> None:
    while True:
        try:
            data.command = data.session.prompt(str(data.prompt))
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