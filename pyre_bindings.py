from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import unix_word_rubout

bindings = KeyBindings()

@bindings.add("c-q")
def _(event):
    event.current_buffer.text = ""

@bindings.add("c-w")
def _(event):
    unix_word_rubout(event)