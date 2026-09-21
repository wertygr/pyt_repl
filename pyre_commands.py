import os
import sys
import types
import datetime
import linecache
import subprocess

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
from pyre_bindings import bindings
from prompt_toolkit import PromptSession

from prompt_toolkit.lexers import PygmentsLexer

def sh_parser(argv: list[str], name_space: dict) -> list[str]:
    result = []
    for arg in argv:
        if arg.startswith("$"):
            if arg[1:] in name_space:
               result.append(str(name_space[arg[1:]]))
            else:
                result.append(arg)
        else:
            result.append(arg)
    return result
def sh(data: Data) -> None:
    shell = data.settings["shell"]
    shell_container = data.settings["shell_container"]
    args = sh_parser(data.argv[1:], data.repl_mode) if shell_container else data.argv[1:]
    try:
        subprocess.run(
            args if not shell else " ".join(args),
            shell=shell
        )
    except FileNotFoundError:
        post(f"[sh]: not file program: {args[0]}", data)

def pyt(data: Data) -> None:
    ev_except = ""
    ex_except = ""
    f_name = register_repl_source(data.postfix, data)
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

    byte_code_ev: types.CodeType|False = byte_code_compile(data.postfix, "eval")
    byte_code_ex: types.CodeType|False = byte_code_compile(data.postfix, "exec")
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
    f_name = register_repl_source(data.postfix, data)
    try:
        exec(compile(data.postfix, f_name, "exec"), data.repl_mode)
    except Exception as e:
        post(e, data)

def pyt_eval(data: Data) ->  None:
    try:
        pft(eval(data.postfix, data.repl_mode), data)
    except Exception as e:
        post(e, data)

@require_args(2)
def source_code(data: Data) -> None:
    obj = data.argv[1]
    flags = data.argv[2:]
    mode = reverse_search_flag({"signature", "code", "dis", "info", "ast"}, flags, "code")
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
        "copy": (lambda: buffer("write", code), True),
        "silent": (lambda: pft(code, data), False),
    }
    flag_mapping(flag_map, flags)

def pyt_pp(data: Data) -> None:
    def read_cache():
        if not data._pyt_plus_old_text:
            with open(f"{PYT_SAVE}/{PYT_CACHE}", "r", encoding="utf-8") as f:
                data._pyt_plus_old_text = f.read()
    def save():
        time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        try:
            with open(f"{PYT_SAVE}/{time_now}.py", "w") as file:
                file.write(data._pyt_plus_old_text)
                print(f"{time_now}.py")
        except Exception as e:
            post(e, data)
    def save_cache():
        if not os.path.isdir(PYT_SAVE):
            os.mkdir(PYT_SAVE)
        with open(f"{PYT_SAVE}/{PYT_CACHE}", "w") as f:
            f.write(data._pyt_plus_old_text)
    def execute():
        if not data._pyt_plus_old_text:
            return
        f_name = register_repl_source(data._pyt_plus_old_text, data)
        ex_code = (
            lambda: pft(eval(compile(data._pyt_plus_old_text, f_name, "eval"), data.repl_mode), data) if "eval" in data.argv
            else exec(compile(data._pyt_plus_old_text, f_name, "eval"), data.repl_mode)
        )
        try:
            ex_code()
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
            data._pyt_plus_old_text = edit_session.prompt(
                line_num(0, 0, 0, data.settings["line_name_format"]),
                default=data._pyt_plus_old_text,
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
            data._pyt_plus_old_text = ""
    if "old" in data.argv:
        read_cache()
    else:
        data._pyt_plus_old_text = ""
    if "paste" in data.argv:
        data._pyt_plus_old_text += buffer("read") # type: ignore
    editor()


    flag_map = {
        "save": (save, True),
        "copy": (lambda: buffer("write", data._pyt_plus_old_text), True),
        "not_exec":(execute, False),
        "not_cache": (save_cache, False)
    }
    flag_mapping(flag_map, data.argv[1:])

@require_args(2)
def shell_command(data: Data) -> None:
    @require_args(3)
    def buffer_command(data: Data):
        write_modes = (lambda mode:
            post(f"[shell_command::buffer_command[{mode}]]: not enough arguments", data) if data.argc < 4 else
            buffer(mode, data.argv[3])
        )
        {
            "read": lambda: pft(buffer("read"), data, end=""),
            "write": lambda: write_modes("write"),
            "write_add":  lambda: write_modes("write_add"),
        }.get(data.argv[2], lambda: post(f"[shell_command::buffer_command]: unknown subcommand: {data.argv[2]}", data))()
    @require_args(3)
    def unload_plug(data: Data):
        for i in data.argv[2:]:
            unload_plugin(i, data)
    @require_args(3)
    def load_plug(data: Data):
        load_plugin(data, data.argv[2])
    @require_args(3)
    def read_vf(data: Data):
        if not(data.argv[2] in linecache.cache):
            e = f"[shell_command::read_vf]: not virtual file: {data.argv[2]}"
            post(e, data)
            return
        text = "".join(linecache.getlines(data.argv[2]))

        flag_map = {
            "copy": (lambda: buffer("write", text), True),
            "silent": (lambda: pft(text, data), False),
        }
        flag_mapping(flag_map, data.argv[1:])
    @require_args(3)
    def del_vf(data: Data):
        for i in data.argv[2:]:
            if not(i in linecache.cache):
                e = f"[shell_command::del_vf]: not virtual file: \"{i}\""
                post(e, data)
                continue
            del linecache.cache[i]
    def list_vf(*_):
        for i in linecache.cache:
            print(f"{i} - {len(''.join(linecache.getlines(i)))} char")
    @require_args(4)
    def hook_run(data: Data):
        hooks_dispatch = data.api["hook_dispatch"]
        hook_name = data.argv[2]
        try:
            # _._ hook_run "name" "{\"test\": \"test hook run\"}"
            hook_arg = eval(data.argv[3], data.repl_mode)
        except Exception as e:
            post(e, data)
            return
        hooks_dispatch(data, hook_name, hook_arg) # type: ignore
    def critical_error(*_):
        raise RuntimeError("critical error in core(tester except)")
    @require_args(3)
    def run_script(data: Data):
        path = data.argv[2]
        try:
            with open(path) as f:
                for i in f:
                    if not i:
                        continue
                    data.command = i
                    data.api["pars_command"](data) # type: ignore
        except Exception as e:
            post(e, data)
    {
        "clear": lambda *_: os.system("cls") if os.name == "nt" else print("\033c"),
        "exit": lambda *_: sys.exit(0),
        "settings_reload": lambda *_: data.api["settings_load"](data, SETTINGS_FILE if data.argc < 3 else data.argv[2]), # type: ignore
        "run": run_script,
        "read_vf": read_vf,
        "ls_vf": list_vf,
        "del_vf": del_vf,
        "unload_plug": unload_plug,
        "critical_error": critical_error,
        "hook_run": hook_run,
        "load_plug": load_plug,
        "buffer": buffer_command,
    }.get(data.argv[1], lambda *_: post(f"[shell_command]: unknown command: {data.argv[1]}", data))(data)