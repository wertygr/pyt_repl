The destructor is a function designed to clean up imported modules and the ["plugin_space"](plugin_space.md).
While the plugin is not required to implement it, doing so is necessary for a complete and proper unload and to support hot reloading.
The loader automatically calls this function during unloading.

<details> <summary> example: </summary>

```python
from plugins.plugin_tools.plugin_types import (PluginApi, CommandContext)

PLUGIN_NAME = "_test_"

def destructor(plugin_space) -> None:
    print("destructor called")
    plugin_space.pop(PLUGIN_NAME, None)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    # init
    if PLUGIN_NAME not in plugin_space:
        plugin_space[PLUGIN_NAME] = {
            "i": 0
        }
    i = plugin_space[PLUGIN_NAME]["i"]
    print(i)
    plugin_space[PLUGIN_NAME]["i"] += 1
```
```pycon
>>> _test_
0
>>> _test_
1
>>> _test_
2
>>> _._ unload_plug _test_
destructor called
>>> _test_
0
>>>
```
</details>
It is also recommended to implement a destructor for modular plugins.
<details> <summary> module example: </summary>

plugin struct:
```text
plugins\
    |-example_plugin\
       |-main.py
       |-utils.py
```

main.py:

```python
import sys
from plugin_tools.plugin_types import (PluginApi, CommandContext)
from plugins.example_plugin.utils import ...

PLUGIN_NAME = "example_plugin"

def destructor(plugin_space) -> None:
    modules = ["plugins.example_plugin.utils"]
    for it in modules:
        sys.modules.pop(it, None)
    plugin_space.pop(PLUGIN_NAME, None)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    ...
```
</details>

<details> <summary> read also </summary>

* [plugin_space](plugin_space.md)
* [\_._ unload_plug](../commands/shell_commands/unload_plug.md)
</details>