import builtins
import keyword

from prompt_toolkit.completion import WordCompleter, NestedCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import beginning_of_line

from simple_shell_lexer import PytLexer
from simple_shell_core import PFT
from simple_shell_core import post
from simple_shell_core import buffer

pyt_lex = PytLexer()


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
def command_dynamics_API(repl_mode):
    try:

        if 'repl_mode' in globals():
            user_variables = [
                name for name in repl_mode.keys()
                if isinstance(name, str) and not name.startswith('_')
            ]

            return dict.fromkeys(user_variables, None)

        return {}
    except Exception as e:
        post(e, 15.0)
        return {}



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


def completer_3():
    try:

        dynamics = command_dynamics_API()
        dynamic_words = list(dynamics.keys()) if dynamics else []


        grammatical_words = []
        if isinstance(grammatical, dict):
            grammatical_words = list(grammatical.keys())
        # elif isinstance(grammatical, (list, tuple, set)):
        #     grammatical_words = list(grammatical)


        python_keywords = keyword.kwlist


        builtins_words = ['print', 'len', 'input', 'range', 'str', 'int', 'dict', 'list', 'set', 'exec', 'eval']


        all_words = set(dynamic_words + grammatical_words + python_keywords + builtins_words)


        clean_words = [word for word in all_words if word and not word.startswith('__')]


        return WordCompleter(clean_words, WORD=True, ignore_case=False)

    except Exception as e:
        PFT(f"{e}\npost_code: 4", pyt_lex)
        return WordCompleter(keyword.kwlist, WORD=True)

def completer(simple_base_command, repl_mode, simple_shell_API_command):
    try:
        dynamics = command_dynamics_API(repl_mode)


        updated_base = dict(simple_base_command)
        updated_base["_pyt-exec_"] = dynamics
        updated_base["_pyt-eval_"] = dynamics
        updated_base["_pyt_"] = dynamics


        modes_and_dynamics = {

            **dict.fromkeys(repl_mode if isinstance(repl_mode, (list, tuple, set)) else [], None),
            **dynamics
        }
        updated_base["_?_"] = modes_and_dynamics

        dynamic_dict = {
            **updated_base,
            **simple_shell_API_command
        }

        return NestedCompleter.from_nested_dict(dynamic_dict)

    except Exception as e:
        post(e, 16.0)
        return NestedCompleter.from_nested_dict(simple_base_command)

