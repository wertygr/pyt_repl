<details> <summary> signature </summary>

```python
def reverse_search_flag(modes: set[str], flags: list[str], def_mode: str)-> str:
    ...
```
</details>

<details> <summary> example </summary>

```python
from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    modes = {"mode_0", "mode_1", "mode_2", "mode_3"}
    flags = command_context["argv"][1:]
    def_mode = "mode_0"
    reverse_search_flag =api["reverse_search_flag"]
    mode = reverse_search_flag(modes, flags, def_mode)
    print(f"current mode: {mode}")
```
```pycon
>>> _test_
current mode: mode_0
>>> _test_ mode_0
current mode: mode_0
>>> _test_ mode_1
current mode: mode_1
>>> _test_ mode_1 mode_0
current mode: mode_0
>>> _test_ mode_1 mode_0 mode_3
current mode: mode_3
>>> _test_ mode_1 mode_0 mode_4
current mode: mode_0
>>>
```

</details>