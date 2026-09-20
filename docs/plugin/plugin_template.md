code in file "plugins/plugin_template.py":
```python
from plugin_tools.plugin_types import (PluginApi, CommandContext, PluginData)
PLUGIN_NAME = "plugin_template"

def destructor(plugin_space) -> None:
    ...

def hook_run(api: PluginApi, hook: str, hook_parameter: dict, plugin_space: dict):
    ...

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    ...
```
in settings:
```json
{
    "plugin": {
        "plugin_template": {
            "file": "plugin_template.py",
            "cache": true,
            "api": true,
            "hooks": []
        }
    }
}
```

<details> <summary> reaf also </summary>

* [API](api/api.md)
* [hook](hook/hook.md)
* [destructor](plugin_destructor.md)
* [plugin specification](plugin_specification.md)
* [plugin space](plugin_space.md)
</details>