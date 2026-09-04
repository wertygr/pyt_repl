#_________________________________________________________________________________________________

import os
import sys
import types
import inspect
import datetime
from string import Template
from typing import Callable

#_________________________________________________________________________________________________

from pyre_plug_load import unload_plugin, _plugin
from pyre_core import PFT, require_args
from pyre_prompt_toolkit import make_jedi_completer
from pyre_core import post
from pyre_core import buffer
from pyre_core import Data
from pyre_core import line_num
from pyre_core import register_repl_source
from pyre_prompt_toolkit import completer_3
from pyre_const import YELLOW
from pyre_const import RESET
from pyre_bindings import bindings

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
    os.system(contr.safe_substitute(data.repl_mode if data.settings.get("shell_container") else {}))

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

@require_args(2)
def source_code(data) -> None:
    _copy = ""
    text = ""

    repl_mode = data.repl_mode
    command_arg = data.command_arg
    try:
        obj = eval(command_arg[1], repl_mode)
        obj = inspect.unwrap(obj)
        if isinstance(obj, Callable):
            while hasattr(obj, "__closure__") and obj.__closure__:
                found_inner = False
                for cell in obj.__closure__:
                    cell_contents = cell.cell_contents
                    if callable(cell_contents):
                        obj = cell_contents
                        found_inner = True
                        break
                if not found_inner:
                    break

    except Exception:
        post(f"[source_code]: not object: {command_arg[1]}", data)
        return
    if callable(obj) or inspect.isclass(obj) or isinstance(obj, types.ModuleType) or inspect.ismodule(obj) or inspect.isfunction(obj) or inspect.isroutine(obj) or inspect.ismethod(obj):
        try:
            _copy = inspect.getsource(obj)
            text = _copy
        except (OSError, TypeError):
            _copy = getattr(obj, "__doc__", "no docstring")
            text = f"[no docstring]"
    else:
        _copy = repr(obj)
        text = f"{command_arg[1]} = {_copy}"

    flag_map = {
        "-copy": [lambda: buffer("paste", text), True],
        "-silent": [lambda: PFT(text, data), False],
    }
    for flag, (action, run_if_present) in flag_map.items():
        is_present = flag in command_arg[1:]

        if is_present == run_if_present:
            action()

def pyt_pp(data: Data):
    def read_cache():
        if not data.pyt_plus_old_text:
            with open("pyt_save/.pyt_save", "r", encoding="utf-8") as f:
                data.pyt_plus_old_text = f.read()
    def save():
        time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        try:
            with open(f"pyt_save/{time_now}.py", "w") as file:
                file.write(data.pyt_plus_old_text)
                print(YELLOW, f"{time_now}.py", RESET)
        except Exception as e:
            post(e, data)
    def save_cache():
        with open("pyt_save/.pyt_save", "w") as f:
            f.write(data.pyt_plus_old_text)
    def execute():
        f_name = register_repl_source(data.pyt_plus_old_text, data)
        try:
            if "eval" in data.command_arg:
                PFT(eval(compile(data.pyt_plus_old_text, f_name, "eval"), data.repl_mode), data)
                return
            exec(compile(data.pyt_plus_old_text, f_name, "exec"), data.repl_mode)
        except Exception as e:
            post(e, data)
    def editor():
        try:
            data.pyt_plus_old_text = prompt(
                line_num(0, 0, 0, data.settings.get("line_name_format", "line_number |")),
                default=data.pyt_plus_old_text,
                completer=make_jedi_completer(data),
                lexer=PygmentsLexer(data.lexer),
                style=data.pt_style,
                multiline=True,
                prompt_continuation=lambda w, h, s: line_num(w, h, s, data.settings.get("line_name_format", "line_number |")),
                key_bindings=bindings
            )
            return
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as e:
            post(e, data)
        data.pyt_plus_old_text = None
    if "old" in data.command_arg:
        read_cache()
    if "paste" in data.command_arg:
        data.pyt_plus_old_text += buffer("copy")

    editor()
    if data.pyt_plus_old_text is None:
        data.pyt_plus_old_text = ""
        return

    flag_map = {
        "save": [save, True],
        "copy": [lambda: buffer("paste", data.pyt_plus_old_text), True],
        "not_exec": [execute, False],
        "not_cache": [save_cache, False]
    }
    for flag, (action, run_if_present) in flag_map.items():
        is_present = flag in data.command_arg[1:]
        if is_present == run_if_present:
            action()

@require_args(2)
def shell_command(data: Data) -> None:
    @require_args(3)
    def unload_plug(data):
        for i in data.command_arg[2:]:
            unload_plugin(i, data)
    @require_args(3)
    def load_plug(data):
        _plugin(data, data.command_arg[2])
    @require_args(4)
    def rname_vf(data):
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
    @require_args(3)
    def n_vf(data):
        data.line_cache.cache[data.command_arg[2]] = (
            0, # memory size
            None, # xz
            "".splitlines(keepends=True),# text
            data.command_arg[2]# name
        )
    @require_args(3)
    def e_vf(data):
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
    @require_args(3)
    def read_vf(data):
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
    @require_args(3)
    def del_vf(data):
        for i in data.command_arg[2:]:
            if not(i in data.line_cache.cache):
                e = f"[shell_command::del_vf]: not virtual file: \"{i}\""
                post(e, data)
                continue
            del data.line_cache.cache[i]

    def list_vf(data):
        for i in data.line_cache.cache:
            print(f"{i} - {len(''.join(data.line_cache.getlines(i)))} char")

    @require_args(4)
    def hook_run(data):
        hooks_dispatch = data.api["hook_dispatch"]
        hook_name = data.command_arg[2]
        try:
            # _._ hook_run "name" "{\"test\": \"test\"}"
            hook_arg = eval(data.command_arg[3], data.repl_mode)
        except Exception as e:
            post(e, data)
            return
        hooks_dispatch(data, hook_name, hook_arg)
    def critical_error(*args):
        raise RuntimeError("critical error in core(tester except)")
    @require_args(3)
    def run_script(data):
        path = data.command_arg[2]

        try:
            with open(path) as file:
                lines = file.readlines()
                for item_2 in lines:
                    if not item_2:
                        continue
                    data.command = item_2
                    data.api["pars_command"](data)
        except Exception as e:
            post(e, data)

    command_map = {
        "clear": lambda *_: os.system("cls" if os.name == "nt" else "clear"),
        "exit": lambda *_: sys.exit(0),
        "settings_reload": lambda *_: data.api["settings_load"](data, ".pyre_settings.json" if data.command_arg_int < 3 else data.command_arg[2]),
        "run": run_script,
        "read_vf": read_vf,
        "ls_vf": list_vf,
        "del_vf": del_vf,
        "rname_vf": rname_vf,
        "n_vf": n_vf,
        "e_vf": e_vf,
        "unload_plug": unload_plug,
        "critical_error": critical_error,
        "hook_run": hook_run,
        "load_plug": load_plug,
    }
    if not(command_map.get(data.command_arg[1])):
        e = f"[shell_command]: unknown command: {data.command_arg[1]}"
        post(e, data)
        return None
    command_map[data.command_arg[1]](data)