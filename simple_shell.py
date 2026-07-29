#________________________________________________________________________________________________

import keyword
import shlex
from pathlib import Path
import datetime
import json
import os
import sys
import linecache

#_________________________________________________________________________________________________

from simple_shell_plug_loader import plugin_ss
from simple_shell_plug_loader import unload_plugin
from simple_shell_plug_loader import plugins_list
from simple_shell_core import PFT
from simple_shell_prompt_toolkit import bindings
from simple_shell_core import post
from simple_shell_commands import source_code
from simple_shell_core import command_separators
from simple_shell_core import alias_parser
from simple_shell_core import alias_list
from simple_shell_core import buffer
from simple_shell_core import Data
from simple_shell_core import line_num
from simple_shell_core import dynamics_completer
from simple_shell_core import register_repl_source
from simple_shell_commands import pyt_eval
from simple_shell_commands import sh
from simple_shell_commands import pyt
from simple_shell_commands import pyt_exec

#_________________________________________________________________________________________________

from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.completion import DynamicCompleter
from prompt_toolkit.completion import WordCompleter
from pygments.token import string_to_tokentype
from prompt_toolkit.styles.pygments import style_from_pygments_dict

#_________________________________________________________________________________________________

BS = "\033[0m"
YELLOW = "\033[33m"

#_________________________________________________________________________________________________

def settings_load(data, file: str = ".simple_shell_settings.json") -> None:
    try:
        with open(file, encoding="utf-8") as f:
            settings = json.load(f)
    except Exception as e:
        context = {
            "e": e,
            "code": 26.0,
            "comment": ""
        }
        post(context, data)
        settings = {}

    line_name_format =    settings.get("line_name_format", "{line_number} |")
    script_file =         settings.get("file", {}).get("script_file", None)

    if isinstance(script_file, str):
        script_file = script_file
    else:
        script_file = None

    data.separator =      settings.get("separator", False)

    data.color_2 =        settings.get("syntax_highlightings", False)
    data.prompt       =    settings.get("simple_shell", ">>> ")

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
    data.pt_style = style_from_pygments_dict(pygments_token_dict)
    data.script_dir       = os.path.dirname(os.path.abspath(__file__))

#_________________________________________________________________________________________________

def plugin_load(data: Data) -> bool:
    if not(data.command_arg[0] in data.settings.get("plugin", {})):
        return False
    plugin_ss(data)
    return True

def completer(data: Data):
    dynamics = dynamics_completer(data) or {}
    if not isinstance(dynamics, dict):
        dynamics = {}

    updated_base = dict(data.simple_base_command)
    updated_base["_pyt-exec_"] = dynamics
    updated_base["_pyt-eval_"] = dynamics
    updated_base["_pyt_"]      = dynamics

    fallback_keys = data.repl_mode if isinstance(data.repl_mode, (list, tuple, set)) else []
    modes_and_dynamics = dict.fromkeys(fallback_keys, None)
    modes_and_dynamics.update(dynamics)
    updated_base["_?_"] = modes_and_dynamics

    dynamic_dict = dict(updated_base)

    return NestedCompleter.from_nested_dict(dynamic_dict)

def completer_3(data: Data):
    dynamics = dynamics_completer(data)
    dynamic_words = list(dynamics.keys()) if dynamics else []

    grammatical_words = []
    if isinstance(data.grammatical, dict):
        grammatical_words = list(data.grammatical.keys())

    builtins_words = ["print", "len", "input", "range", "str", "int", "dict", "list", "set", "exec", "eval"]
    all_words = set(dynamic_words + grammatical_words + keyword.kwlist + builtins_words)
    clean_words = [word for word in all_words if word and not word.startswith("__")]

    return WordCompleter(clean_words, WORD=True, ignore_case=False)

# // ________________________________________________________________________________________________

def shell_command(data: Data) -> None:
    if data.command_arg_int < 2:
        e = "[shell_command]: not enough arguments"
        context = {
            "e": e,
            "code": 7.8,
            "comment": ""
        }
        post(context, data)
        return None

    def unload_plug():
        if data.command_arg_int < 3:
            e = "[shell_command::unload_plug]: not enough arguments"
            context = {
                "e": e,
                "code": 7.9,
                "comment": ""
            }
            post(context, data)
            return
        for i in data.command_arg[2:]:
            unload_plugin(i, data)

    def rname_vf():
        if data.command_arg_int < 4:
            e = "[shell_command::rname_vf]: not enough arguments"
            context = {
                "e": e,
                "code": 7.12,
                "comment": ""
            }
            post(context, data)
            return
        if not(data.command_arg[2] in data.line_cache.cache):
            e = "[shell_command::rname_vf]: not virtual file: " + data.command_arg[2]
            context = {
                "e": e,
                "code": 7.13,
                "comment": ""
            }
            post(context, data)
            return
        if data.command_arg[3] in data.line_cache.cache:
            e = f"[shell_command::rname_vf] file name: \"{data.command_arg[3]}\" taken"
            context = {
                "e": e,
                "code": 7.14,
                "comment": ""
            }
            post(context, data)
            return
        data.line_cache.cache[data.command_arg[3]] = (
            len(
                "".join(
                    data.line_cache.getlines(
                        data.command_arg[2]
                    )
                )
            ), None, "".join(
            data.line_cache.getlines(
                data.command_arg[2]
            )
        ).splitlines(keepends=True), data.command_arg[3])
        del data.line_cache.cache[data.command_arg[2]]

    def n_vf():
        if data.command_arg_int < 3:
            e = "[shell_command::n_vf]: not enough arguments"
            context = {
                "e": e,
                "code": 7.15,
                "comment": ""
            }
            post(context, data)
            return
        data.line_cache.cache[data.command_arg[2]] = (
            0, # memory size
            None, # xz
            "".splitlines(keepends=True),# text
            data.command_arg[2]# name
        )

    def e_vf():
        if data.command_arg_int < 3:
            e = "[shell_command::e_vf]: not enough arguments"
            context = {
                "e": e,
                "code": 7.17,
                "comment": ""
            }
            post(context, data)
            return
        if not(data.command_arg[2] in data.line_cache.cache):
            e = "[shell_command::e_vf]: not virtual file: " + data.command_arg[2]
            context = {
                "e": e,
                "code": 7.18,
                "comment": ""
            }
            post(context, data)
            return
        try:
            text = prompt(
                line_num(0, 0, 0, data),
                default= "".join(data.line_cache.getlines(data.command_arg[2])),
                completer=completer_3(data),
                lexer=PygmentsLexer(data.lexer),
                style=data.pt_style,
                multiline=True,
                prompt_continuation=lambda w ,h, s: line_num(w, h, s, data),
                key_bindings=bindings
            )
            data.line_cache.cache[data.command_arg[2]] = (
                len(text), None, text.splitlines(keepends=True), data.command_arg[2]
            )
        except (KeyboardInterrupt, EOFError):
            pass

    def read_vf():
        if data.command_arg_int < 3:
            e = "[shell_command::read_vf]: not enough arguments"
            context = {
                "e": e,
                "code": 7.7,
                "comment": ""
            }
            post(context, data)
            return
        if not(data.command_arg[2] in data.line_cache.cache):
            e = "[shell_command::read_vf]: not virtual file: " + data.command_arg[2]
            context = {
                "e": e,
                "code": 7.6,
                "comment": ""
            }
            post(context, data)
            return
        text = "".join(data.line_cache.getlines(data.command_arg[2]))

        flag_map = {
            "-copy": [lambda: buffer("paste", text), True],
            "-silent": [lambda: PFT(text, data), False],
        }
        for flag, (action, run_if_present) in flag_map.items():
            is_present = flag in data.command_arg[1:]

            if is_present == run_if_present:
                action()

    def del_vf():
        if data.command_arg_int < 3:
            e = "[shell_command::del_vf]: not enough arguments"
            context = {
                "e": e,
                "code": 7.9,
                "comment": ""
            }
            post(context, data)
            return
        for i in data.command_arg[2:]:
            if not(i in data.line_cache.cache):
                e = "[shell_command::del_vf]: not virtual file: " + i
                context = {
                    "e": e,
                    "code": 7.10,
                    "comment": ""
                }
                post(context, data)
                continue
            del data.line_cache.cache[i]


    def list_vf():
        for i in data.line_cache.cache:
            print(i)

    def edit_open_dir() -> None:
        if data.command_arg_int < 2:
            return None
        path = Path(data.command_arg[2]).resolve()

        if Path(path).is_dir():
            os.chdir(path)

    def alias_list_interlayer():
        alias_list(data.settings)
    def help_ss():
        with open(Path(__file__).resolve(), "r", encoding="utf-8") as f:
            PFT(f.read(), data)
            return

    def SSS():
        if data.command_arg_int < 2:
            return None
        path = data.command_arg[2]

        try:
            with open(path) as file:
                lines = file.readlines()
                for item_2 in lines:
                    if item_2 == "":
                        continue
                    pars_command(item_2)
        except Exception as e:
            context = {
                "e": e,
                "code": 7.2,
                "comment": ""
            }
            post(context, data)


    command_map = {
        "clear": lambda: os.system("cls" if os.name == "nt" else "clear"),
        "exit": lambda: sys.exit(0),
        "settings_reload": lambda: settings_load(data),
        "plugins_list": lambda: plugins_list(data),
        "alias_list": alias_list_interlayer,
        "run": SSS,
        "help": help_ss,
        "history_del": lambda: os.remove(".ss_history"),
        "open": edit_open_dir,
        "read_vf": read_vf,
        "ls_vf": list_vf,
        "del_vf": del_vf,
        "rname_vf": rname_vf,
        "n_vf": n_vf,
        "e_vf": e_vf,
        "unload_plug": unload_plug
    }
    if not(command_map.get(data.command_arg[1])):
        e = f"[shell_command]: unknown command: {data.command_arg[1]}"
        context = {
            "e": e,
            "code": 7.11,
            "comment": ""
        }
        post(context, data)
        return None
    command_map[data.command_arg[1]]()



def pyt_pp(data: Data) -> None:
    code = ""
    def save():
        time_now = str(datetime.datetime.now().strftime("%H_%M_%S"))
        try:
            with open(f"pyt_save/{time_now}.py", "w") as file:
                file.write(code)
                print(YELLOW, f"{time_now}.py", BS)
        except Exception as e:
            context = {
                "e": e,
                "code": 11.4,
                "comment": ""
            }
            post(context, data)

    def execute():
        f_name = register_repl_source(code, data)
        try:
            exec(compile(code, f_name, "exec"), data.repl_mode)
        except Exception as e:
            context = {
                "e": e,
                "code": 11.2,
                "comment": ""
            }
            post(context, data)

    if "old" in data.command_arg:
        if data.pyt_plus_old_text == "":
            with open("pyt_save/.pyt_save", "r", encoding="utf-8") as f:
                data.pyt_plus_old_text = f.read()
    else:
        data.pyt_plus_old_text = ""
    if "paste" in data.command_arg:
        data.pyt_plus_old_text += buffer("copy")


    try:
        code = prompt(
            line_num(0, 0, 0, data),
            default=data.pyt_plus_old_text,
            completer=DynamicCompleter(lambda: completer_3(data)),
            lexer=PygmentsLexer(data.lexer),
            style=data.pt_style,
            multiline=True,
            prompt_continuation=lambda w ,h, s: line_num(w, h, s, data),
            key_bindings=bindings
        )

        if not ("not_cache" in data.command_arg):
            pyt_plus_old_text = code
            try:
                if not (Path("pyt_save/.pyt_save").is_file()):
                    with open("pyt_save/.pyt_save", "x", encoding="utf-8") as f:
                        f.write(pyt_plus_old_text)
                else:
                    with open("pyt_save/.pyt_save", "w") as f:
                        f.write(pyt_plus_old_text)
            except Exception as e:
                context = {
                    "e": e,
                    "code": 11.3,
                    "comment": ""
                }
                post(context, data)
    except (KeyboardInterrupt , EOFError):
        pass
    except Exception as e:
        context = {
            "e": e,
            "code": 11.0,
            "comment": ""
        }
        post(context, data)

    flag_map = {
        "save": [save, True],
        "copy": [lambda: buffer("paste", pyt_plus_old_text), True],
        "not_exec": [execute, False],
    }
    for flag, (action, run_if_present) in flag_map.items():
        is_present = flag in data.command_arg[1:]
        if is_present == run_if_present:
            action()

#_________________________________________________________________________________________________

def dispatcher(data: Data) -> None:
    if not data.command_arg:
        e = "[dispatcher]: empty command"
        context = {
            "e": e,
            "code": 22.0,
            "comment": ""
        }
        post(context, data)
        return None
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
        "crit":           lambda *args : 1/0,
    }
    func = command_map.get(data.command_arg[0])
    if func:
        func(data)
    elif plugin_load(data):
        pass
    else:
        e = f"[dispatcher]: unknown command: {data.command_arg[0]}"
        context = {
            "e": e,
            "code": 22.1,
            "comment": ""
        }
        post(context, data)

# // _______________________________________________________________________________________________________

def pars_command(data: Data) -> None:
    if data.settings.get("shlex", False):
        try:
            data.command_arg = shlex.split(data.command, posix=bool(data.settings.get("posix", False)))
        except ValueError as e:
            context = {
                "e": e,
                "code": 14.1,
                "comment": ""
            }
            post(context, data)
            return None
    else:
        data.command_arg = data.command.split()
    data.command_arg_int = len(data.command_arg)
    if data.command_arg_int < 1:
        e = "[pars_command]: not enough arguments"
        context = {
            "e": e,
            "code": 14.0,
            "comment": ""
        }
        post(context, data)
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

# // ______________________________________________________________________________________________________

def initialisation() -> Data:
    data = Data()
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
        "BS": BS,
        "YELLOW": YELLOW,
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
    return data

def main():
    data = initialisation()

    history_command = FileHistory(".ss_history")
    session = PromptSession(
        completer=DynamicCompleter(lambda: completer(data)),
        multiline=data.settings.get("multiline", False),
        lexer=PygmentsLexer(data.lexer),
        style=data.pt_style,
        prompt_continuation=lambda w, h, s : line_num(w, h, s, data),
        history=history_command,
        include_default_pygments_style = False
    )
    while True:
        try:
            data.command = session.prompt(str(data.prompt))
            pars_command(data)
        except (EOFError, KeyboardInterrupt):
            pass
        except Exception as e:
            context = {
                "e": e,
                "code": 19.0,
                "comment": ""
            }
            post(context, data)
            return

if __name__ == "__main__":
    main()