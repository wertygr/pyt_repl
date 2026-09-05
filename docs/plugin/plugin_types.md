recommendation:
```python
from plugins.plugin_tools.types import (PluginData, PluginApi, CommandContext)

def hook_run(api: PluginApi, hook: str, hook_parameter: dict, plugin_space: dict):
    ...

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    ...
```