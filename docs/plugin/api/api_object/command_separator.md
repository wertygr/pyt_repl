<details><summary>command_separator: example code and use</summary>

```python
from plugins.plugin_tools.types import (PluginData, PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    post = api["post"]
    data = api["data"]
    command_separators = api["command_separators"]

    if command_context["command_arg_int"] < 2:
        post("[_example_plugin_::main]: not enough arguments", data)
        return {}
    commands = command_separators(command_context["command_arg"][1].split())
    print(f"command_arg: {command_context['command_arg']}\ncommands: {commands}\n__")
    for i in commands:
        print(i)
```

```pycon
>>> _#_ data.settings["shlex"] == True = True; data.settings["posix"] == True = True
>>> _example_plugin_ "command_1 _&_ command2 _&_ command3"
command_arg: ['_example_plugin_', 'command_1 _&_ command2 _&_ command3']
commands: [['command_1'], ['command2'], ['command3']]
__
['command_1']
['command2']
['command3']
>>>
```

</details>