import os
from string import Template
import inspect
import types

from simple_shell_core import Data
from simple_shell_core import register_repl_source
from simple_shell_core import post
from simple_shell_core import PFT
from simple_shell_core import buffer
from simple_shell_core import YELLOW
from simple_shell_core import BS


def pyt_eval(data: Data) ->  None:
    try:
        result_eval = eval(data.command_prefix, data.repl_mode)
        PFT(result_eval, data)
    except Exception as e:
        context = {
            "e": e,
            "code": 9.0,
            "comment": ""
        }
        post(context, data)
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
            print(eval(byte_code_ev, data.repl_mode))
        except Exception as e:
            context = {
                "e": e,
                "code": 8.2,
                "comment": ""
            }
            post(context, data)
    elif byte_code_ex:
        try:
            exec(byte_code_ex, data.repl_mode)
        except Exception as e:
            context = {
                "e": e,
                "code": 8.1,
                "comment": ""
            }
            post(context, data)
    else:
        context = {
            "e": f"{"-"*15}\neval: {ev_except}\n{"-"*15}\nexec: {ex_except}\n{"-"*15}",
            "code": 8.0,
            "comment": ""
        }
        post(context, data)

def pyt_exec(data: Data) -> None:
    f_name = register_repl_source(data.command_prefix, data)
    try:
        exec(compile(data.command_prefix, f_name, "exec"), data.repl_mode)
    except Exception as e:
        context = {
            "e": e,
            "code": 10.0,
            "comment": ""
        }
        post(context, data)


def source_code(data) -> None:
    _copy = ""
    text = ""
    repl_mode = data.repl_mode
    command_arg = data.command_arg
    command_arg_int = data.command_arg_int
    ss_style = data.pt_style
    if command_arg_int < 2:
        e = "[source_code]: not enough arguments"
        context = {
            "e": e,
            "code": 27.0,
            "comment": ""
        }
        post(context, data)
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
        context = {
            "e": e,
            "code": 27.1,
            "comment": ""
        }
        post(context, data)

    flag_map = {
        "-copy": [lambda: buffer("paste", text), True],
        "-silent": [lambda: PFT(text, data), False],
    }
    for flag, (action, run_if_present) in flag_map.items():
        is_present = flag in command_arg[1:]

        if is_present == run_if_present:
            action()
