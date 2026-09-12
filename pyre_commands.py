#_________________________________________________________________________________________________

import os
import sys
import types
import datetime
import linecache
from string import Template

#_________________________________________________________________________________________________

from pyre_plug_load import (unload_plugin, load_plugin)
from pyre_prompt_toolkit import make_jedi_completer
from pyre_bottom_toolbar import (bottom_toolbar)
from pyre_core import (
    post,
    buffer,
    Data,
    line_num,
    register_repl_source,
    pft,
    require_args,
    traceback_format,
    flag_mapping,
    reverse_search_flag
)
from pyre_const import (
    SETTINGS_FILE, PYT_SAVE, PYT_CACHE
)
from pyre_inspect import get_source_code, PyreInspectError
from pyre_const import YELLOW, RESET
from pyre_bindings import bindings
from prompt_toolkit import PromptSession

#_________________________________________________________________________________________________

from prompt_toolkit.lexers import PygmentsLexer

#_________________________________________________________________________________________________

def pyt_eval(data: Data) ->  None:
    try:
        result_eval = eval(data.command_prefix, data.repl_mode)
        pft(result_eval, data)
    except Exception as e:
        post(e, data)
def sh (data: Data) -> None:
    contr = Template(data.command_prefix)
    os.system(contr.safe_substitute(data.repl_mode if data.settings["shell_container"] else {}))

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

    byte_code_ev: types.CodeType|False = byte_code_compile(data.command_prefix, "eval")
    byte_code_ex: types.CodeType|False = byte_code_compile(data.command_prefix, "exec")
    if byte_code_ev:
        try:
            pft(eval(byte_code_ev, data.repl_mode), data)
        except Exception as e:
            post(e, data)
    elif byte_code_ex:
        try:
            exec(byte_code_ex, data.repl_mode)
        except Exception as e:
            post(e, data)
    else:
        e = f"{'__ '*15} \neval: \n{traceback_format(ev_except)} \n{'__ '*15}\nexec: \n{traceback_format(ex_except)} \n{'__ '*15}"
        post(e, data)

def pyt_exec(data: Data) -> None:
    f_name = register_repl_source(data.command_prefix, data)
    try:
        exec(compile(data.command_prefix, f_name, "exec"), data.repl_mode)
    except Exception as e:
        post(e, data)

@require_args(2)
def source_code(data: Data) -> None:
    obj = data.command_arg[1]
    flags = data.command_arg[2:]
    mode = reverse_search_flag(("signature", "normal", "dis", "info"), flags, "normal")
    code = get_source_code(
        obj_name=obj,
        namespace=data.repl_mode,
        mode=mode,
        use_unwrap= "unwrap" in flags,
        use_closure= "closure" in flags,
    )
    if isinstance(code, PyreInspectError):
        post(f"[source_code]: {str(code)}", data)
        return
    flag_map = {
        "copy": (lambda: buffer("paste", code), True),
        "silent": (lambda: pft(code, data), False),
    }
    flag_mapping(flag_map, data.command_arg[1:])

def pyt_pp(data: Data) -> None:
    def read_cache():
        if not data.pyt_plus_old_text:
            with open(f"{PYT_SAVE}/{PYT_CACHE}", "r", encoding="utf-8") as f:
                data.pyt_plus_old_text = f.read()
    def save():
        time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        try:
            with open(f"{PYT_SAVE}/{time_now}.py", "w") as file:
                file.write(data.pyt_plus_old_text)
                print(YELLOW, f"{time_now}.py", RESET)
        except Exception as e:
            post(e, data)
    def save_cache():
        with open(f"{PYT_SAVE}/{PYT_CACHE}", "w") as f:
            f.write(data.pyt_plus_old_text)
    def execute():
        f_name = register_repl_source(data.pyt_plus_old_text, data)
        try:
            if "eval" in data.command_arg:
                pft(eval(compile(data.pyt_plus_old_text, f_name, "eval"), data.repl_mode), data)
                return
            exec(compile(data.pyt_plus_old_text, f_name, "exec"), data.repl_mode)
        except Exception as e:
            post(e, data)
    def editor():
        edit_session = PromptSession(
            key_bindings=bindings,
        )
        edit_session.app.data = data
        edit_session.app.mode = "pyt++"
        toolbar = lambda: bottom_toolbar(data)
        try:
            data.pyt_plus_old_text = edit_session.prompt(
                line_num(0, 0, 0, data.settings["line_name_format"]),
                default=data.pyt_plus_old_text,
                completer=make_jedi_completer(data),
                lexer=PygmentsLexer(data.lexer),
                style=data.pt_style,
                multiline=True,
                prompt_continuation=lambda w, h, s: line_num(w, h, s, data.settings["line_name_format"]),
                vi_mode=data.settings["vi_mode"],
                mouse_support=data.settings["mouse_support"],
                bottom_toolbar=toolbar() if data.settings["bottom_toolbar"] else None,
            )
        except (KeyboardInterrupt, EOFError):
            data.pyt_plus_old_text = ""

    if "old" in data.command_arg:
        read_cache()
    else:
        data.pyt_plus_old_text = ""
    if "paste" in data.command_arg:
        data.pyt_plus_old_text += buffer("copy") # type: ignore
    editor()


    flag_map = {
        "save": (save, True),
        "copy": (lambda: buffer("paste", data.pyt_plus_old_text), True),
        "not_exec":(execute, False),
        "not_cache": (save_cache, False)
    }
    flag_mapping(flag_map, data.command_arg[1:])

@require_args(2)
def shell_command(data: Data) -> None:
    @require_args(3)
    def unload_plug(data: Data):
        for i in data.command_arg[2:]:
            unload_plugin(i, data)
    @require_args(3)
    def load_plug(data: Data):
        load_plugin(data, data.command_arg[2])
    @require_args(3)
    def read_vf(data: Data):
        if not(data.command_arg[2] in linecache.cache):
            e = "[shell_command::read_vf]: not virtual file: " + data.command_arg[2]
            post(e, data)
            return
        text = "".join(linecache.getlines(data.command_arg[2]))

        flag_map = {
            "-copy": (lambda: buffer("paste", text), True),
            "-silent": (lambda: pft(text, data), False),
        }
        flag_mapping(flag_map, data.command_arg[1:])
    @require_args(3)
    def del_vf(data: Data):
        for i in data.command_arg[2:]:
            if not(i in linecache.cache):
                e = f"[shell_command::del_vf]: not virtual file: \"{i}\""
                post(e, data)
                continue
            del linecache.cache[i]
    def list_vf(data):
        for i in data.line_cache.cache:
            print(f"{i} - {len(''.join(data.line_cache.getlines(i)))} char")
    @require_args(4)
    def hook_run(data: Data):
        hooks_dispatch = data.api["hook_dispatch"]
        hook_name = data.command_arg[2]
        try:
            # _._ hook_run "name" "{\"test\": \"test hook run\"}"
            hook_arg = eval(data.command_arg[3], data.repl_mode)
        except Exception as e:
            post(e, data)
            return
        hooks_dispatch(data, hook_name, hook_arg) # type: ignore
    def critical_error(*_):
        raise RuntimeError("critical error in core(tester except)")
    @require_args(3)
    def run_script(data: Data):
        path = data.command_arg[2]
        try:
            with open(path) as f:
                for i in f:
                    if not i:
                        continue
                    data.command = i
                    data.api["pars_command"](data) # type: ignore
        except Exception as e:
            post(e, data)
    command_map = {
        "clear": lambda *_: os.system("cls") if os.name == "nt" else print("\033c"),
        "exit": lambda *_: sys.exit(0),
        "settings_reload": lambda *_: data.api["settings_load"](data, SETTINGS_FILE if data.command_arg_int < 3 else data.command_arg[2]), # type: ignore
        "run": run_script,
        "read_vf": read_vf,
        "ls_vf": list_vf,
        "del_vf": del_vf,
        "unload_plug": unload_plug,
        "critical_error": critical_error,
        "hook_run": hook_run,
        "load_plug": load_plug,
    }
    command_map.get(data.command_arg[1], lambda *_: post(f"[shell_command]: unknown command: {data.command_arg[1]}", data))(data)