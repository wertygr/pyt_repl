# // ________________________________________________________________________________________________

import builtins
import inspect
import keyword
import shlex
from pathlib import Path
from string import Template

# // _________________________________________________________________________________________________

import ast
import datetime
import json
import os
import sys
import subprocess

# // ___________________________________

from simple_shell_plug_loader import plugin_ss
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
from simple_shell_core import register_repl_source

# // ____________________________________

from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.completion import DynamicCompleter
from prompt_toolkit.completion import WordCompleter

# // ___________________________________________________________________________________________________

exceptions = {e for e in dir(builtins) if 'Error' in e or 'Exception' in e}
exceptions = dict.fromkeys(exceptions)
functions = {name for name in dir(builtins) if name[0].islower()}
functions = dict.fromkeys(functions)
keywords = keyword.kwlist
keywords = dict.fromkeys(keywords)

grammatical = {
    **functions,
    **keywords,
    **exceptions
}

local_repl_mode = {}

script_dir = os.path.dirname(os.path.abspath(__file__))

ERR = "\033[31m"
BS = "\033[0m"
YELLOW = "\033[33m"

# // ____________________________________________________________________________________________________

pyt_lex = PytLexer()
def settings_load(file: str = f"{script_dir}/.simple_shell_settings.json") -> None:
    global color_container, line_name_format, script_file, separator, color_2, simple_shell, settings, repl_mode, shell_container

    default_settings = {
            "color": {
                "color": True,

                "prefix": "#C77DBB",
                "string": "#6AAB73",
                "number": "#2AACB8",
                "keyword": "bold #CF8E6D",
                "comment": "italic #7A7E85",
                "name": "#BCBEC4",
                "operator": "#cccccc",
                "punctuation": "#ffffff",
                "text": "#cccccc",
                "def_name": "#56A8F5",
                "error": "underline #D64D5B",
                "action": "#8888C6"
            },
            "line_name_format": "{line_number:>{width}} |",
            "file": {},
            "simple_shell": ">>> ",
            "prefix": {},
            "plugin": {},
            "plugin_loader_mode": "globals",
            "ss_api": True,
            "separator": True,
            "cache": True,
            "repl_mode": "globals",
            "shell_container": True,
            "shlex": False,
            "multiline": False,
            "alias_globals": True,
            "alias_locals": True,
            "posix": True,
            "alias_dict": {}
        }

    try:
        with open(file, encoding="utf-8") as f:
            settings = json.load(f)
    except Exception as e:
        post(e, -1.0)
        settings = {}

    color = settings.get("color", {}) # // optimization
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
        script_file = script_file.format(script_dir=script_dir)
    else:
        script_file = None

    separator =           settings.get("separator", False)

    color_2 =             settings.get("color", {}).get("color", True)
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
        repl_mode = globals()
    else:
        repl_mode = local_repl_mode

    if settings.get("shell_container", False):
        shell_container = repl_mode
    else:
        shell_container = {}

settings_load()

# // ___________________________________________________________________________________________________

def command_dynamics_API():
    try:

        if 'repl_mode' in globals():

            user_variables = [
                name for name in repl_mode.keys()
                if isinstance(name, str) and not name.startswith('_')
            ]

            return dict.fromkeys(user_variables, None)

        return {}
    except Exception as e:
        post(e, -2.0)
        return {}


simple_base_command = {
    "_#_": None,
    "_pyt_": grammatical,
    "_pyt-exec_": grammatical,
    "_pyt-eval_": grammatical,
    "_&_": None,
    "_?_": command_dynamics_API(),
    "_._": {
        "exit": None,
        "clear": None,
        "history_del": None,
        "settings_reload": None,
        "plugins_list": None,
        "run_script": {
            "{script_dir}": None
        },
        "debug": None,
        "help": None
    },
    "_pyt++_": {
        "old": None
    },
    "_sh_": None,

    **dict.fromkeys(settings.get("plugin", {}), None),
    **dict.fromkeys(settings.get("alias_dict", {}), None),
    **dict.fromkeys(settings.get("prefix", {}).get("prefix_run", {}), None),
}


# // ___________________________________________________________________________________________________

pt_style = make_ss_style(color_container)

# // ___________________________________________________________________________________________________


def plugin_load(
        command_prefix,
        command_arg_int,
        command_arg,
    ) -> bool|plug:
    global plug
    if command_arg[0] in settings["plugin"]:
        plug = plugin_ss(
            command_prefix,
            command_arg_int,
            command_arg,

            plugin=command_arg[0],
            name_space=repl_mode,
            ss_api=ss_api
        )
        return True
    else:
        return False


def prefix_commands_run(prefix, command_prefix_run) -> bool:
    if prefix in settings["prefix"]:
        prefix_value = settings["prefix"][prefix]
        try:
            if isinstance(prefix_value, dict):
                path = prefix_value["path"].format(script_dir=script_dir)
                program = prefix_value["program"].format(python = sys.executable)
                command_type = prefix_value["command"]
                if command_type:
                    subprocess.run([program, path, command_prefix_run])
                else:
                    subprocess.run([program, path])
            else:
                try:
                    try:
                        subprocess.run([prefix_value, command_prefix_run])
                    except:
                        print(eval(prefix_value))
                        subprocess.run([eval(prefix_value), command_prefix_run])
                except Exception as e:
                    post(e, 1.0)
        except Exception as e:
            post(e, 1.1)
        return True
    else:
        return False


def line_num(
        width=0,
        line_number=0,
        is_soft_wrap=0,
    ) -> None:
    return line_name_format.format(
        width=width,
        line_number=line_number + 1,
        is_soft_wrap=is_soft_wrap
    )


def command_ast(shell_command_API):
    if script_file != None:
        try:
            with open(script_file, "r", encoding="utf-8") as file:
                text = file.read()
            tree_shell = ast.parse(text)

            for node in ast.walk(tree_shell):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == shell_command_API:
                            print(shell_command_API)
                            return ast.literal_eval(node.value)

        except Exception as e:
            post(e, 2.0)
            return {"none_command": None}


simple_shell_API_command = command_ast("simple_shell_command_API")

def completer():
    try:

        dynamics = command_dynamics_API() or {}
        if not isinstance(dynamics, dict):
            dynamics = {}

        updated_base = dict(simple_base_command)
        updated_base["_pyt-exec_"] = dynamics
        updated_base["_pyt-eval_"] = dynamics
        updated_base["_pyt_"]      = dynamics

        fallback_keys = repl_mode if isinstance(repl_mode, (list, tuple, set)) else []
        modes_and_dynamics = dict.fromkeys(fallback_keys, None)


        modes_and_dynamics.update(dynamics)
        updated_base["_?_"] = modes_and_dynamics


        dynamic_dict = dict(updated_base)
        if isinstance(simple_shell_API_command, dict):
            dynamic_dict.update(simple_shell_API_command)
        def fix_for_nested_completer(d):
            if not isinstance(d, dict):
                return None

            cleaned = {}
            for k, v in d.items():
                if v == {}:
                    cleaned[k] = None
                elif isinstance(v, dict) and len(v) > 0:
                    cleaned[k] = fix_for_nested_completer(v)

                else:
                    cleaned[k] = v
            return cleaned

        safe_dynamic_dict = fix_for_nested_completer(dynamic_dict)

        return NestedCompleter.from_nested_dict(safe_dynamic_dict)

    except Exception as e:
        post(e, 3.0)
        return NestedCompleter.from_nested_dict({})


def completer_3():
    try:

        dynamics = command_dynamics_API()
        dynamic_words = list(dynamics.keys()) if dynamics else []


        grammatical_words = []
        if isinstance(grammatical, dict):
            grammatical_words = list(grammatical.keys())
        elif isinstance(grammatical, (list, tuple, set)):
            grammatical_words = list(grammatical)


        python_keywords = keyword.kwlist


        builtins_words = ['print', 'len', 'input', 'range', 'str', 'int', 'dict', 'list', 'set', 'exec', 'eval']


        all_words = set(dynamic_words + grammatical_words + python_keywords + builtins_words)


        clean_words = [word for word in all_words if word and not word.startswith('__')]


        return WordCompleter(clean_words, WORD=True, ignore_case=False)

    except Exception as e:
        post(e, 4.0)
        return WordCompleter(keyword.kwlist, WORD=True)
# // ________________________________________________________________________________________________


def sh (command_prefix, *args) -> None:
    try:
        contr = Template(command_prefix)
        os.system(contr.safe_substitute(shell_container))
    except Exception as e:
        post(e, 5.0)


def shell_command(command_prefix, command_arg_int, command_arg, *args) -> None:
    if command_arg_int < 2:
        return None

    def edit_open_dir() -> None:

        if command_arg_int < 2:
            return None
        path = Path(command_arg[2]).resolve()

        if Path(path).is_dir():
            os.chdir(path)



    def alias_list_interlayer():
        alias_list(settings)
    def help_ss():
        function = None
        if command_arg_int > 2:
            function = command_arg[2]
        else:
            with open(Path(__file__).resolve(), "r", encoding="utf-8") as f:
                PFT(f.read(), pt_style)
                return
        if isinstance(function, str):
            found_object = repl_mode.get(function)

            if found_object is None:
                post(function, 7.5)
                return
            function = found_object
            print(function)

        try:
            source = inspect.getsource(function)
            PFT(source, pt_style)
        except TypeError as e:
            post(e, 7.4)
        except OSError as e:
            post(e, 7.3)

    def SSS():
        if command_arg_int < 2:
            return None
        path = command_arg[2].format(script_dir = script_dir)

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
        "history_del": lambda: os.remove(f"{script_dir}/.ss_history"),
        "open": edit_open_dir
    }

    if command_map.get(command_arg[1]):
        command_map[command_arg[1]]()


def pyt(command_prefix, *args) -> None:
    ev_except = ""
    ex_except = ""
    f_name = register_repl_source(command_prefix)
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

    byte_code_ev = byte_code_compile(command_prefix, "eval")
    byte_code_ex = byte_code_compile(command_prefix, "exec")
    if byte_code_ev:
        try:
            print(eval(byte_code_ev, repl_mode))
        except Exception as e:
            post(e, 8.2)
    elif byte_code_ex:
        try:
            exec(byte_code_ex, repl_mode)
        except Exception as e:
            post(e, 8.1)
    else:
        post(f"{"-"*15}\neval: {ev_except}\n{"-"*15}\nexec: {ex_except}\n{"-"*15}", 8.0)



def pyt_eval(command_prefix, *args) ->  None:
    try:
        result_eval = eval(command_prefix, repl_mode)
        PFT(result_eval,pt_style ,pyt_lex)
    except Exception as e:
        post(e, 9.0)


def pyt_exec(command_prefix, *args) -> None:
    f_name = register_repl_source(command_prefix)
    try:
        exec(compile(command_prefix, f_name, 'exec'), repl_mode)
    except Exception as e:
        post(e, 10.0)
def pyt_pp(arg, command_arg_int: int, command_arg: list, *args) -> None:
    global pyt_plus_old_text
    if "old" in command_arg:
        if pyt_plus_old_text == "":
            with open(f"{script_dir}/pyt_save/.pyt_save", "r", encoding="utf-8") as f:
                pyt_plus_old_text = f.read()
    else:
        pyt_plus_old_text = ""
    if "paste" in command_arg:
        pyt_plus_old_text += buffer("copy")


    try:
        code = prompt(
            line_num(),
            default=pyt_plus_old_text,
            completer=completer_3(),
            lexer=PygmentsLexer(PytLexer),
            style=pt_style,
            multiline=True,
            prompt_continuation=line_num,
            key_bindings=bindings
        )

        if not ("not_cache" in command_arg):
            pyt_plus_old_text = code
            try:
                if not (Path(f"{script_dir}/pyt_save/.pyt_save").is_file()):
                    with open(f"{script_dir}/pyt_save/.pyt_save", "x", encoding="utf-8") as f:
                        f.write(str(pyt_plus_old_text))
                else:
                    with open(f"{script_dir}/pyt_save/.pyt_save", "w") as f:
                        f.write(str(pyt_plus_old_text))
            except Exception as e:
                post(e, 11.3)
        if "save" in command_arg:
            now = datetime.datetime.now()
            time_now = str(now.strftime("%H_%M_%S"))
            try:
                with open(f"{script_dir}/pyt_save/{time_now}.py", "w") as file:
                    file.write(code)
                print(YELLOW, f"{time_now}.py", BS)
            except Exception as e:
                post(e, 11.4)
        if not ("not_exec" in command_arg):
            try:
                f_name = register_repl_source(code)
                try:
                    exec(compile(code, f_name, 'exec'), repl_mode)
                except Exception as e:
                    post(e, 11.2)
            except Exception as e:
                post(e, 11.1)
        if "copy" in command_arg:
            buffer("paste", pyt_plus_old_text)
    except (KeyboardInterrupt , EOFError):
        pass
    except Exception as e:
        post(e, 11.0)

# // _________________________________________________________________________________________________________

pyt_plus_old_text = ""
history_command = FileHistory(".ss_history")

# // _________________________________________________________________________________________________________

def dispatcher(command_arg: list) -> None:
    if command_arg == []:
        post("empty command list", 22.0)
        return None
    command_prefix = " ".join(command_arg[1:])
    command_arg_int = len(command_arg)

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
    func = command_map.get(command_arg[0])
    if func:
        func(
            command_prefix,
            command_arg_int,
            command_arg,
            repl_mode,
            pt_style
        )

    elif prefix_commands_run(command_arg[0], command_prefix):
        pass
    elif plugin_load(
            command_prefix,
            command_arg_int,
            command_arg,
        ):
        pass
    else:
        fallback_script_run(settings.get("file", {}), command_arg)

# // _______________________________________________________________________________________________________

frame = sys._getframe()

def pars_command(command) -> None:
    if settings.get("shlex", False):
        try:
            command_arg = shlex.split(command, posix=is_posix(settings))
        except ValueError as e:
            post(e, 14.1)
            return None
    else:
        command_arg = command.split()
    command_arg_int = len(command_arg)
    if command_arg_int < 1:
        e = "[pars_command]: not enough arguments"
        post(e, 14.0)
        return None
    if settings.get("alias_globals", False):
        command_arg = alias_parser(settings.get("alias_dict", {}), command_arg, "global")
    if separator:
        commands = command_separators(command_arg)
        for i in commands:
            if settings.get("alias_locals", False):
                i = alias_parser(settings.get("alias_dict", {}), i, "local")
            dispatcher(i)
    else:
        if settings.get("alias_locals", False):
            i = alias_parser(settings.get("alias_dict", {}), command_arg, "local")
        else:
            i = command_arg
        dispatcher(i)


# // ______________________________________________________________________________________________________

ss_api = {

    "ERR": ERR,
    "BS": BS,
    "YELLOW": YELLOW,
    "color_container": color_container,

    "settings": settings,
    "simple_shell": simple_shell,

    "script_dir": script_dir,
    "script_file": script_file,

    "pyt_lex": pyt_lex,
    "pt_style": pt_style,

    "post": post,
    "PFT": PFT,
    "is_posix": is_posix,
    "command_separators": command_separators,
    "pars_command": pars_command,
    "dispatcher": dispatcher,
    "buffer": buffer,
    "alias_parser": alias_parser
}

# // ______________________________________________________________________________________________________

def main() -> int:
    try:
        session = PromptSession(
            completer=DynamicCompleter(completer),
            multiline=settings.get("multiline", False),
            lexer=PygmentsLexer(PytLexer),
            style=pt_style,
            prompt_continuation=line_num,
            history=history_command
        )
        while True:
            if color_2:
                command = session.prompt(str(simple_shell))
            else:
                command = input(simple_shell)
            pars_command(command)

    except KeyboardInterrupt:
        return 0
    except Exception as e:
        post(e, 19.0)
        breakpoint()
        return -1

if __name__ == "__main__":
    main()