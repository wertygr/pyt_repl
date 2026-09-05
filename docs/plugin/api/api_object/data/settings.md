<details> <summary>settings: example code and use</summary>

```python
from plugins.plugin_tools.types import (PluginData, PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space):
    data = api["data"]
    if len(command_context["command_arg"]) < 2:
        new_prompt = ">>>> "
    else:
        new_prompt = command_context["command_arg"][1]
    data.settings["prompt"] = new_prompt
```

```pycon
>>> _#_ settings.md["shlex"] == True = True
>>> _example_plugin_ :>>>
:>>>_example_plugin_ ":>>> "
:>>> _example_plugin_ ">>> "
>>> _example_plugin_
>>>>
```
</details>


<details> <summary> read also </summary> 

* [.pyre_settings.json](../../../../settings/settings.md)

</details>