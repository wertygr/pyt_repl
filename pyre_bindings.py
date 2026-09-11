from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.named_commands import unix_word_rubout
from prompt_toolkit.application import run_in_terminal

bindings = KeyBindings()

@bindings.add("c-q")
def _(event):
    buffer = event.current_buffer
    buffer.text = ""

@bindings.add("c-w")
def _(event):
    unix_word_rubout(event)

@bindings.add("c-t")
async def open_console(event):
    data = event.app.data
    if event.app.mode != "pyt++":
        return
    def secondary_prompt():
        secondary_data = input()
        data.command = secondary_data
        data.api["pars_command"](data)
    await run_in_terminal(secondary_prompt)