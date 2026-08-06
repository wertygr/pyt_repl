#_________________________________________________________________________________________________

import os
import sys
import types
import inspect
import datetime
from pathlib import Path
from string import Template

#_________________________________________________________________________________________________

from pyre_plug_load import unload_plugin
from pyre_plug_load import plugins_list
from pyre_core import PFT
from pyre_prompt_toolkit import bindings, make_jedi_completer
from pyre_core import post
from pyre_core import alias_list
from pyre_core import buffer
from pyre_core import Data
from pyre_core import line_num
from pyre_core import register_repl_source
from pyre_core import settings_load
from pyre_prompt_toolkit import completer_3
from pyre_core import YELLOW
from pyre_core import BS

#_________________________________________________________________________________________________

from prompt_toolkit import prompt
from prompt_toolkit.lexers import PygmentsLexer

#_________________________________________________________________________________________________

def pyt_eval(data: Data) ->  None:
    try:
        result_eval = eval(data.command_prefix, data.repl_mode)
        PFT(result_eval, data)
    except Exception as e:
        post(e, data)
def sh (data: Data) -> None:
    contr = Template(data.command_prefix)
    os.system(contr.safe_substitute(data.shell_container))

def pyt(data: Data) -> None:
    ev_except = ""
    ex_except = ""
    f_name = register_repl_source(data.command_prefix, data)
    def byte_code_compile(code: str, mode: str):
        nonlocal ev_except, ex_except
        try:
            return compile(code, f_name, mode)
        except Exception as e:
            if mode == "exec":
                ex_except = e
            else:
                ev_except = e
            return False

    byte_code_ev = byte_code_compile(data.command_prefix, "eval")
    byte_code_ex = byte_code_compile(data.command_prefix, "exec")
    if byte_code_ev:
        try:
            PFT(eval(byte_code_ev, data.repl_mode), data)
        except Exception as e:
            post(e, data)
    elif byte_code_ex:
        try:
            exec(byte_code_ex, data.repl_mode)
        except Exception as e:
            post(e, data)
    else:
        e = f"{'__ '*15} \neval: {ev_except} \n{'__ '*15}\nexec: {ex_except} \n{'__ '*15}"
        post(e, data)

def pyt_exec(data: Data) -> None:
    f_name = register_repl_source(data.command_prefix, data)
    try:
        exec(compile(data.command_prefix, f_name, "exec"), data.repl_mode)
    except Exception as e:
        post(e, data)


def source_code(data) -> None:
    _copy = ""
    text = ""

    repl_mode = data.repl_mode
    command_arg = data.command_arg
    command_arg_int = data.command_arg_int
    if command_arg_int < 2:
        e = "[source_code]: not enough arguments"
        post(e, data)
        return
    obj = repl_mode.get(command_arg[1])

    if callable(obj) or inspect.isclass(obj) or isinstance(obj, types.ModuleType):
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
        e = f"[source_code]: no object: {command_arg[1]}"
        post(e, data)

    flag_map = {
        "-copy": [lambda: buffer("paste", text), True],
        "-silent": [lambda: PFT(text, data), False],
    }
    for flag, (action, run_if_present) in flag_map.items():
        is_present = flag in command_arg[1:]

        if is_present == run_if_present:
            action()


def pyt_pp(data: Data) -> None:
    code = ""
    def save():
        time_now = str(datetime.datetime.now().strftime("%H_%M_%S"))
        try:
            with open(f"pyt_save/{time_now}.py", "w") as file:
                file.write(code)
                print(YELLOW, f"{time_now}.py", BS)
        except Exception as e:
            post(e, data)

    def execute():
        f_name = register_repl_source(code, data)
        try:
            if "eval" in data.command_arg:
                PFT(eval(compile(code, f_name, "eval"), data.repl_mode), data)
                return
            exec(compile(code, f_name, "exec"), data.repl_mode)
        except Exception as e:
            post(e, data)

    if "old" in data.command_arg:
        if data.pyt_plus_old_text == "":
            with open("pyt_save/.pyt_save", "r", encoding="utf-8") as f:
                data.pyt_plus_old_text = f.read()
        else: data.pyt_plus_old_text = data.pyt_plus_old_text
    else:
        data.pyt_plus_old_text = ""
    if "paste" in data.command_arg:
        data.pyt_plus_old_text += buffer("copy")


    try:
        code = prompt(
            line_num(0, 0, 0, data),
            default=data.pyt_plus_old_text,
            completer=make_jedi_completer(data),
            lexer=PygmentsLexer(data.lexer),
            style=data.pt_style,
            multiline=True,
            prompt_continuation=lambda w ,h, s: line_num(w, h, s, data),
            key_bindings=bindings
        )

        if not ("not_cache" in data.command_arg):
            data.pyt_plus_old_text = code
            try:
                with open("pyt_save/.pyt_save", "w") as f:
                    f.write(data.pyt_plus_old_text)
            except Exception as e:
                post(e, data)
    except (KeyboardInterrupt , EOFError):
        pass
    except Exception as e:
        post(e, data)

    flag_map = {
        "save": [save, True],
        "copy": [lambda: buffer("paste", data.pyt_plus_old_text), True],
        "not_exec": [execute, False],
    }
    for flag, (action, run_if_present) in flag_map.items():
        is_present = flag in data.command_arg[1:]
        if is_present == run_if_present:
            action()

def shell_command(data: Data) -> None:
    if data.command_arg_int < 2:
        e = "[shell_command]: not enough arguments"
        post(e, data)
        return None

    def unload_plug():
        if data.command_arg_int < 3:
            e = "[shell_command::unload_plug]: not enough arguments"
            post(e, data)
            return
        for i in data.command_arg[2:]:
            unload_plugin(i, data)

    def rname_vf():
        if data.command_arg_int < 4:
            e = "[shell_command::rname_vf]: not enough arguments"
            post(e, data)
            return
        if not(data.command_arg[2] in data.line_cache.cache):
            e = "[shell_command::rname_vf]: not virtual file: " + data.command_arg[2]
            post(e, data)
            return
        if data.command_arg[3] in data.line_cache.cache:
            e = f"[shell_command::rname_vf] file name: \"{data.command_arg[3]}\" taken"
            post(e, data)
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
            post(e, data)
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
            post(e, data)
            return
        if not(data.command_arg[2] in data.line_cache.cache):
            e = "[shell_command::e_vf]: not virtual file: " + data.command_arg[2]
            post(e, data)
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
            post(e, data)
            return
        if not(data.command_arg[2] in data.line_cache.cache):
            e = "[shell_command::read_vf]: not virtual file: " + data.command_arg[2]
            post(e, data)
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
            post(e, data)
            return
        for i in data.command_arg[2:]:
            if not(i in data.line_cache.cache):
                e = f"[shell_command::del_vf]: not virtual file: \"{i}\""
                post(e, data)
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
        with open(data.repl_file, "r", encoding="utf-8") as f:
            PFT(f.read(), data)
            return

    def critical_error(*args):
        raise RuntimeError("critical error in core(tester except)")

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
                    data.ss_api["pars_command"](item_2)
        except Exception as e:
            post(e, data)


    command_map = {
        "clear": lambda: os.system("cls" if os.name == "nt" else "clear"),
        "exit": lambda: sys.exit(0),
        "settings_reload": lambda: settings_load(data),
        "plugins_list": lambda: plugins_list(data),
        "alias_list": alias_list_interlayer,
        "run": SSS,
        "help": help_ss,
        "history_del": lambda: os.remove(".py_history"),
        "open": edit_open_dir,
        "read_vf": read_vf,
        "ls_vf": list_vf,
        "del_vf": del_vf,
        "rname_vf": rname_vf,
        "n_vf": n_vf,
        "e_vf": e_vf,
        "unload_plug": unload_plug,
        "critical_error": critical_error
    }
    if not(command_map.get(data.command_arg[1])):
        e = f"[shell_command]: unknown command: {data.command_arg[1]}"
        post(e, data)
        return None
    command_map[data.command_arg[1]]()