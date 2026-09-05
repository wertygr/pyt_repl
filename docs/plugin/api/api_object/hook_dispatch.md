Plugins can call hooks via the API.

<details> <summary> example code</summary> 

```python
from plugins.plugin_tools.types import (PluginData, PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    hooks_dispatch = api["hook_dispatch"]
    data = api["data"]
    hook_parametr = {}
    hooks_dispatch(data, "hook_name", hook_parametr)
```

</details>