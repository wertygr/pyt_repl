#_________________________________________________________________________________________________

import builtins
import keyword

#_________________________________________________________________________________________________

from simple_shell_core import buffer
from simple_shell_core import Data
from simple_shell_core import dynamics_completer

#_________________________________________________________________________________________________

import jedi
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import beginning_of_line
from prompt_toolkit.completion import Completion
from prompt_toolkit.completion import DynamicCompleter
from prompt_toolkit.completion import Completer

#_________________________________________________________________________________________________


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
bindings = KeyBindings()

@bindings.add('tab', 'q')
def _(event):
    event.current_buffer.insert_text('    ')


@bindings.add('tab', '/')
def _(event):
    beginning_of_line(event)
    _buffer = event.current_buffer


    _buffer.insert_text('# ')

@bindings.add('tab', 'd')
def _(event):
    _buffer = event.current_buffer
    document = _buffer.document

    from_position = document.get_start_of_line_position()
    to_position = document.get_end_of_line_position()

    if document.cursor_position + to_position < len(document.text):
        to_position += 1
    elif document.cursor_position + from_position > 0:
        from_position -= 1

    _buffer.delete_before_cursor(-from_position)
    _buffer.delete(to_position - from_position)

@bindings.add("escape", "c-c")
def _(event):
    if event.app.current_buffer.selection_state is not None:
        select = event.current_buffer.copy_selection()
        buffer("add", select)

@bindings.add("c-v")
def _(event):
    _buffer = event.current_buffer
    _buffer.insert_text(buffer())

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
    return WordCompleter(all_words, WORD=True, ignore_case=False)

def completer_5(data: Data) -> str:
    text = ""
    for i in range(data._repl_cache_id + 1):
        f_name = f"<simple_shell_repl_{i}>"
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
    completer = DynamicCompleter(lambda: JediCompleter(data))
    return completer