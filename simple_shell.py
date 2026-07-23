# // ________________________________________________________________________________________________

import builtins
import keyword
import shlex
from pathlib import Path
from string import Template
import ast
import datetime
import json
import os
import sys
import linecache

# // _________________________________________________________________________________________________

from simple_shell_plug_loader import plugin_ss, unload_plugin
from simple_shell_plug_loader import plugins_list
from simple_shell_lexer import PytLexer
from simple_shell_core import PFT
from simple_shell_prompt_toolkit import bindings
from simple_shell_core import post
from simple_shell_core import source_code
from simple_shell_core import command_separators
from simple_shell_core import make_ss_style
from simple_shell_core import is_posix
from simple_shell_core import fallback_script_run
from simple_shell_core import alias_parser
from simple_shell_core import alias_list
from simple_shell_core import buffer

# // ____________________________________

from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.completion import DynamicCompleter
from prompt_toolkit.completion import WordCompleter

# // ___________________________________________________________________________________________________

class Data:
    simple_base_command ={}
    grammatical = {
        **dict.fromkeys({name for name in dir(builtins) if name[0].islower()}),
        **dict.fromkeys(keyword.kwlist),
        **dict.fromkeys({e for e in dir(builtins) if "Error" in e or "Exception" in e})
    }
    repl_mode = {}
    local_repl_mode = {}
    _repl_cache_id = 0
    pyt_lex = PytLexer()
    color_container = {}
    line_name_format = ""
    script_file = ""
    separator = False
    color_2 = False
    simple_shell = ""
    settings = {}
    shell_container = {}
    pt_style = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))

    ss_api = {}

    command = ""
    pyt_plus_old_text = ""

    command_prefix = ""
    command_arg_int = 0
    command_arg = []



ERR = "\033[31m"
BS = "\033[0m"
YELLOW = "\033[33m"

# // ____________________________________________________________________________________________________

def register_repl_source(source: str, data) -> str:
    data._repl_cache_id += 1
    filename = f"<simple_shell_repl_{data._repl_cache_id}>"
    linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
    return filename

def settings_load(data, file: str = ".simple_shell_settings.json") -> None:
    try:
        with open(file, encoding="utf-8") as f:
            settings = json.load(f)
    except Exception as e:
        post(e, 26.0)
        settings = {}

    color = settings.get("color", {})
    prefix_color =        color.get("prefix", "#C77DBB")
    string_color =        color.get("string", "#6A7E85")
    number_color =        color.get("number", "#2AACB8")
    keyword_color =       color.get("keyword", "#2AACB8")
    comment_color =       color.get("comment", "italic #7A7E85")
    name_color =          color.get("name", "#BCBEC4")
    operator_color =      color.get("operator", "#cccccc")
    punctuation_color =   color.get("punctuation", "#ffffff")
    text_color =          color.get("text", "#CCCCCC")
    def_name_color =      color.get("def_name", "#56A8F5")
    error_color =         color.get("error", "underline #D64D5B")
    action_color =        color.get("action", "#8888C6")

    line_name_format =    settings.get("line_name_format", "{line_number} |")
    script_file =         settings.get("file", {}).get("script_file", None)
    if isinstance(script_file, str):
        script_file = script_file
    else:
        script_file = None

    data.separator =      settings.get("separator", False)

    data.color_2 =        settings.get("color", {}).get("color", True)
    simple_shell =        settings.get("simple_shell", ">>> ")
    repl_mode_text =      settings.get("repl_mode", "locals")


    color_container = {
        "prefix":      prefix_color,
        "string":      string_color,
        "number":      number_color,
        "keyword":     keyword_color,
        "comment":     comment_color,
        "name":        name_color,
        "operator":    operator_color,
        "punctuation": punctuation_color,
        "text":        text_color,
        "def_name":    def_name_color,
        "error":       error_color,
        "action":      action_color
    }

    if repl_mode_text == "globals":
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
    data.color_container  = color_container
    data.simple_shell     = simple_shell
    data.pt_style         = make_ss_style(color_container)

# // ___________________________________________________________________________________________________

def command_dynamics_API(data: Data):
    return dict.fromkeys(
        [
            name for name in data.repl_mode.keys()
            if isinstance(name, str)
        ],
        None
    )

# // ___________________________________________________________________________________________________

def plugin_load(data: Data) -> bool:
    if not(data.command_arg[0] in data.settings["plugin"]):
        return False
    plugin_ss(
        data.command_prefix,
        data.command_arg_int,
        data.command_arg,

        plugin     =  data.command_arg[0],
        name_space = data.repl_mode,
        ss_api     = data.ss_api
    )
    return True

def line_num(
        width: int,
        line_number: int,
        is_soft_wrap: int,
        data: Data
    ) -> str:
    return data.line_name_format.format(
         width=width,
         line_number=line_number + 1,
         is_soft_wrap=is_soft_wrap
    )


def command_ast(shell_command_API: str, data: Data) -> dict:
    if data.script_file == None:
        return {"": None}
    try:
        with open(data.script_file, "r", encoding="utf-8") as file:
            text = file.read()
        tree_shell = ast.parse(text)
    except Exception as e:
        post(e, 2.0)
        return {"": None}
    for node in ast.walk(tree_shell):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == shell_command_API:
                    print(shell_command_API)
                    return ast.literal_eval(node.value)
    return {"": None}

def completer(data: Data):
    dynamics = command_dynamics_API(data) or {}
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
    dynamics = command_dynamics_API(data)
    dynamic_words = list(dynamics.keys()) if dynamics else []

    grammatical_words = []
    if isinstance(data.grammatical, dict):
        grammatical_words = list(data.grammatical.keys())

    builtins_words = ["print", "len", "input", "range", "str", "int", "dict", "list", "set", "exec", "eval"]
    all_words = set(dynamic_words + grammatical_words + keyword.kwlist + builtins_words)
    clean_words = [word for word in all_words if word and not word.startswith("__")]

    return WordCompleter(clean_words, WORD=True, ignore_case=False)

# // ________________________________________________________________________________________________


def sh (data: Data) -> None:
    contr = Template(data.command_prefix)
    os.system(contr.safe_substitute(data.shell_container))

def shell_command(data: Data) -> None:
    if data.command_arg_int < 2:
        e = "[shell_command]: not enough arguments"
        post(e, 7.8)
        return None

    def unload_plug():
        if data.command_arg_int < 3:
            e = "[shell_command::unload_plug]: not enough arguments"
            post(e, 7.9)
            return
        for i in data.command_arg[2:]:
            unload_plugin(i)

    def rname_vf():
        if data.command_arg_int < 4:
            e = "[shell_command::rname_vf]: not enough arguments"
            post(e, 7.12)
            return
        if not(data.command_arg[2] in linecache.cache):
            e = "[shell_command::rname_vf]: not virtual file: "+data.command_arg[2]
            post(e, 7.13)
            return
        if data.command_arg[3] in linecache.cache:
            e = f"[shell_command::rname_vf] file name: \"{data.command_arg[3]}\" taken"
            post(e, 7.14)
            return
        linecache.cache[data.command_arg[3]] = (
            len(
                "".join(
                    linecache.getlines(
                        data.command_arg[2]
                    )
                )
            ), None, "".join(
            linecache.getlines(
                data.command_arg[2]
            )
        ).splitlines(keepends=True), data.command_arg[3])
        del linecache.cache[data.command_arg[2]]

    def n_vf():
        if data.command_arg_int < 3:
            e = "[shell_command::n_vf]: not enough arguments"
            post(e, 7.15)
            return
        linecache.cache[data.command_arg[2]] = (
            0, # memory size
            None, # xz
            "".splitlines(keepends=True),# text
            data.command_arg[2]# name
        )

    def e_vf():
        if data.command_arg_int < 3:
            e = "[shell_command::e_vf]: not enough arguments"
            post(e, 7.17)
            return
        if not(data.command_arg[2] in linecache.cache):
            e = "[shell_command::e_vf]: not virtual file: " + data.command_arg[2]
            post(e, 7.18)
            return
        try:
            text = prompt(
                line_num(0, 0, 0, data),
                default= "".join(linecache.getlines(data.command_arg[2])),
                completer=completer_3(data),
                lexer=PygmentsLexer(PytLexer),
                style=data.pt_style,
                multiline=True,
                prompt_continuation=lambda w ,h, s: line_num(w, h, s, data),
                key_bindings=bindings
            )
            linecache.cache[data.command_arg[2]] = (
                len(text), None, text.splitlines(keepends=True), data.command_arg[2]
            )
        except (KeyboardInterrupt, EOFError):
            pass

    def read_vf():
        if data.command_arg_int < 3:
            e = "[shell_command::read_vf]: not enough arguments"
            post(e, 7.7)
            return
        if not(data.command_arg[2] in linecache.cache):
            e = "[shell_command::read_vf]: not virtual file: " + data.command_arg[2]
            post(e, 7.6)
            return
        text = "".join(linecache.getlines(data.command_arg[2]))

        flag_map = {
            "-copy": [lambda: buffer("paste", text), True],
            "-silent": [lambda: PFT(text, data.pt_style), False],
        }
        for flag, (action, run_if_present) in flag_map.items():
            is_present = flag in data.command_arg[1:]

            if is_present == run_if_present:
                action()

    def del_vf():
        if data.command_arg_int < 3:
            e = "[shell_command::del_vf]: not enough arguments"
            post(e, 7.9)
            return
        for i in data.command_arg[2:]:
            if not(i in linecache.cache):
                e = "[shell_command::del_vf]: not virtual file: " + i
                post(e, 7.10)
                continue
            del linecache.cache[i]


    def list_vf():
        for i in linecache.cache:
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
            PFT(f.read(), data.pt_style)
            return

    def SSS():
        if data.command_arg_int < 2:
            return None
        path = data.command_arg[2]

        try:
            with open(path) as file:
                lines = file.readlines()
                for item_2 in lines:
                    pars_command(item_2)
        except Exception as e:
            post(e, 7.2)


    command_map = {
        "clear": lambda: os.system('cls' if os.name == 'nt' else 'clear'),
        "exit": lambda: sys.exit(0),
        "settings_reload": settings_load,
        "plugins_list": plugins_list,
        "alias_list": alias_list_interlayer,
        "run": SSS,
        "help": help_ss,
        "history_del": lambda: os.remove(".ss_history"),
        "open": edit_open_dir,
        "read_vf": read_vf,
        "list_vf": list_vf,
        "del_vf": del_vf,
        "rname_vf": rname_vf,
        "n_vf": n_vf,
        "e_vf": e_vf,
        "unload_plug": unload_plug
    }
    if not(command_map.get(data.command_arg[1])):
        e = f"[shell_command]: unknown command: {data.command_arg[1]}"
        post(e, 7.11)
        return None
    command_map[data.command_arg[1]]()


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
            post(e, 8.2)
    elif byte_code_ex:
        try:
            exec(byte_code_ex, data.repl_mode)
        except Exception as e:
            post(e, 8.1)
    else:
        post(f"{"-"*15}\neval: {ev_except}\n{"-"*15}\nexec: {ex_except}\n{"-"*15}", 8.0)



def pyt_eval(data: Data) ->  None:
    try:
        result_eval = eval(data.command_prefix, data.repl_mode)
        PFT(result_eval, data.pt_style ,data.pyt_lex)
    except Exception as e:
        post(e, 9.0)


def pyt_exec(data: Data) -> None:
    f_name = register_repl_source(data.command_prefix, data)
    try:
        exec(compile(data.command_prefix, f_name, 'exec'), data.repl_mode)
    except Exception as e:
        post(e, 10.0)
def pyt_pp(data: Data) -> None:
    code = ""
    def save():
        time_now = str(datetime.datetime.now().strftime("%H_%M_%S"))
        try:
            with open(f"pyt_save/{time_now}.py", "w") as file:
                file.write(code)
                print(YELLOW, f"{time_now}.py", BS)
        except Exception as e:
            post(e, 11.4)

    def execute():
        f_name = register_repl_source(code, data)
        try:
            exec(compile(code, f_name, 'exec'), data.repl_mode)
        except Exception as e:
            post(e, 11.2)

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
            lexer=PygmentsLexer(PytLexer),
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
                post(e, 11.3)
    except (KeyboardInterrupt , EOFError):
        pass
    except Exception as e:
        post(e, 11.0)

    flag_map = {
        "save": [save, True],
        "copy": [lambda: buffer("paste", pyt_plus_old_text), True],
        "not_exec": [execute, False],
    }
    for flag, (action, run_if_present) in flag_map.items():
        is_present = flag in data.command_arg[1:]
        if is_present == run_if_present:
            action()

# // _________________________________________________________________________________________________________

pyt_plus_old_text = ""
history_command = FileHistory(".ss_history")

# // _________________________________________________________________________________________________________

def dispatcher(data: Data) -> None:
    if data.command_arg == []:
        post("empty command list", 22.0)
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
        "_#_":        lambda *args :    None
    }
    func = command_map.get(data.command_arg[0])
    if func:
        func(data)
    elif plugin_load(data):
        pass
    else:
        fallback_script_run(data.settings.get("file", {}), data.command_arg)

# // _______________________________________________________________________________________________________

def pars_command(data: Data) -> None:
    if data.settings.get("shlex", False):
        try:
            data.command_arg = shlex.split(data.command, posix=is_posix(data.settings))
        except ValueError as e:
            post(e, 14.1)
            return None
    else:
        data.command_arg = data.command.split()
    data.command_arg_int = len(data.command_arg)
    if data.command_arg_int < 1:
        e = "[pars_command]: not enough arguments"
        post(e, 14.0)
        return None
    if data.settings.get("alias_globals", False):
        data.command_arg = alias_parser(data.settings.get("alias_dict", {}), data.command_arg, "global")
    if data.separator:
        commands = command_separators(data.command_arg)
        for i in commands:
            if data.settings.get("alias_locals", False):
                data.command_arg = alias_parser(data.settings.get("alias_dict", {}), i, "local")
            dispatcher(data)
    else:
        if data.settings.get("alias_locals", False):
            i = alias_parser(data.settings.get("alias_dict", {}), data.command_arg, "local")
        else:
            i = data.command_arg
        dispatcher(data)

# // ______________________________________________________________________________________________________

def main() -> int:
    data = Data()
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
        **dict.fromkeys(data.settings.get("prefix", {}).get("prefix_run", {}), None),
        **command_ast("simple_shell_command_API", data)
    }
    data.ss_api = {

        "ERR": ERR,
        "BS": BS,
        "YELLOW": YELLOW,
        "color_container": data.color_container,

        "settings": data.settings,
        "simple_shell": data.simple_shell,

        "script_dir": data.script_dir,
        "script_file": data.script_file,

        "pyt_lex": data.pyt_lex,
        "pt_style": data.pt_style,

        "post": post,
        "PFT": PFT,
        "is_posix": is_posix,
        "command_separators": command_separators,
        "pars_command": pars_command,
        "dispatcher": dispatcher,
        "buffer": buffer,
        "alias_parser": alias_parser,
        "data": data
    }


    session = PromptSession(
        completer=DynamicCompleter(lambda: completer(data)),
        multiline=data.settings.get("multiline", False),
        lexer=PygmentsLexer(PytLexer),
        style=data.pt_style,
        prompt_continuation=lambda w, h, s : line_num(w, h, s, data),
        history=history_command
    )
    while True:
        try:
            if data.color_2:
                data.command = session.prompt(str(data.simple_shell))
            else:
                data.command = input(data.simple_shell)
            pars_command(data)
        except (EOFError, KeyboardInterrupt):
            pass
        except Exception as e:
            post(e, 19.0)
            return -1

if __name__ == "__main__":
    main()