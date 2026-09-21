This function is necessary for the correct operation of introspection with dynamically created objects.

<details> <summary> signature </summary>

```python
def register_repl_source(source: str, data: Data) -> str:
    ...
```
</details>

<details> <summary> example </summary>

```python
from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    register_repl_source = api["register_repl_source"]
    data = api["data"]
    code = """
def test():
    pass
    """
    f_name = register_repl_source(code, data)
    exec(compile(code, f_name, "exec"), data.repl_mode)
```
```pycon
>>> _?_ test
[source_code]: no object test

>>> _test_
>>> _?_ test
def test():
    pass

>>>
```
</details>