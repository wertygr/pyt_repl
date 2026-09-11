dynamic settings reload

<details> <summary> signature: </summary>

```python
def settings_load(data: Data, file: str = SETTINGS_FILE) -> None:
    ...
```
</details>

<details> <summary> example: </summary>

```python
from plugins.plugin_tools.plugin_types import PluginApi, CommandContext

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    data = api["data"]
    settings_load = api["settings_load"]
    settings_load(data)
```
```pycon
>>> _test_
|>>>
```

</details>

<details> <summary> read also: </summary>

* [settings](../../../settings/settings.md)
</details>