example:

plugin struct
```text
plugins
 |-example_plugin
    |-main.py
    |-utils.py
```

main.py:

```python
import sys
from plugin_tools.plugin_types import (PluginApi, PluginData, CommandContext)
from plugins.example_plugin.utils import ...

PLUGIN_NAME = "example_plugin"

def destructor(plugin_space) -> None:
    moduls = ["plugins.example_plugin.utils"]
    for it in moduls:
        del sys.modules[it]
    del plugin_space[PLUGIN_NAME]

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    ...
```