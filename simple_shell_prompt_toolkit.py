import builtins
import keyword

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import beginning_of_line
from simple_shell_core import buffer


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