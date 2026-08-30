#_________________________________________________________________________________________________

import builtins
import keyword

#_________________________________________________________________________________________________

from pyre_core import Data

#_________________________________________________________________________________________________

import jedi
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import Completion
from prompt_toolkit.completion import DynamicCompleter
from prompt_toolkit.completion import Completer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import unix_word_rubout

#_________________________________________________________________________________________________

grammatical = {
        **dict.fromkeys({name for name in dir(builtins) if name[0].islower()}),
        **dict.fromkeys(keyword.kwlist),
        **dict.fromkeys({e for e in dir(builtins) if "Error" in e or "Exception" in e})
}
def create_base_command(settings: dict) -> dict[str, None|dict]:
    return {
            "_#_": None,
            "_pyt_": None,
            "_pyt-exec_": None,
            "_pyt-eval_": None,
            "_&_": None,
            "_?_": None,
            "_._": {
                "exit": None,
                "clear": None,
                "history_del": None,
                "settings_reload": None,
                "run": {
                    "{script_dir}": None
                },
                "help": None,
                "ls_vf": None,
                "read_vf": None,
                "rname_vf": None
            },
            "_pyt++_": {
                "old": None
            },
            "_sh_": None,

            **dict.fromkeys(settings.get("plugin", {}), None),
            **dict.fromkeys(settings.get("alias_dict", {}), None),
        }

bindings = KeyBindings()

@bindings.add("c-q")
def _(event):
    buffer = event.current_buffer
    buffer.text = ""

@bindings.add("c-w")
def _(event):
    unix_word_rubout(event)

def dynamics_completer(data: Data):
    return {
        **dict.fromkeys(data.repl_mode, None),
        **grammatical
    }

def completer(data: Data):
    dynamics = dynamics_completer(data) or {}
    if not isinstance(dynamics, dict):
        dynamics = {}

    updated_base = create_base_command(data.settings)
    updated_base["_pyt-exec_"] = dynamics
    updated_base["_pyt-eval_"] = dynamics
    updated_base["_pyt_"]      = dynamics
    updated_base["_._"]["read_vf"] = dict.fromkeys(data.line_cache.cache, None)
    updated_base["_._"]["del_vf"] = updated_base["_._"]["read_vf"]
    updated_base["_._"]["unload_plug"] = dict.fromkeys(data.settings.get("plugin", {}), None)

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
    if isinstance(grammatical, dict):
        grammatical_words = list(grammatical.keys())

    builtins_words = [name for name in dir(builtins) if name[0].islower()]
    all_words = set(dynamic_words + grammatical_words + keyword.kwlist + builtins_words)
    return WordCompleter(all_words, WORD=True, ignore_case=False)

def completer_5(data: Data) -> str:
    text = ""
    for i in range(data._repl_cache_id + 1):
        f_name = f"<py_repl_{i}>"
        if not(f_name in data.line_cache.cache):
            continue
        text = text + "".join(data.line_cache.getlines(f_name)) + "\n"
    return text

def jedi_completer(document, complete_event, data):
    history_text = completer_5(data)
    current_text = document.text

    full_code = history_text + current_text
    history_lines = history_text.count("\n")

    cursor_row = (document.cursor_position_row + 1) + history_lines
    cursor_col = document.cursor_position_col

    try:
        script = jedi.Script(code=full_code)
        for comp in script.complete(cursor_row, cursor_col):
            already_typed_len = len(comp.name) - len(comp.complete)
            yield Completion(
                text=comp.name,
                start_position=-already_typed_len,
                display=comp.name,
                display_meta=comp.type
            )
    except:
        return

class JediCompleter(Completer):
    def __init__(self, data):
        self.data = data

    def get_completions(self, doc, ev):
        pass

    async def get_completions_async(self, doc, ev):
        for completion in jedi_completer(doc, ev, self.data):
            yield completion

def make_jedi_completer(data):
    return DynamicCompleter(lambda: JediCompleter(data))