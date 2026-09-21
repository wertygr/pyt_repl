This function is required to output errors to the console with syntax highlighting(Python);
it is a simple wrapper around [pft](pft.md).

<details> <summary> signature </summary> 

```python
def post(e: TracebackType|BaseException|str, data: Data, use_hook: bool = True) -> None:
    ...
```

| parametr | description |
|:---------|------------:|

</details>

<details> <summary> example </summary>

```python
from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    data = api["data"]
    post = api["post"]
    try:
        bad_var = 0 / 0
    except Exception as e:
        post(e, data)
        print("\n", data.last_error)
    """
    post signature - post(e: Any, data: Data)
    """
```

```pycon
>>> _test_
Traceback (most recent call last):
  File ".../plugins/test.py", line 5, in main
    bad_var = 0/0
              ~^~
ZeroDivisionError: division by zero


 Traceback (most recent call last):
  File ".../plugins/test.py", line 5, in main
    bad_var = 0/0
              ~^~
ZeroDivisionError: division by zero

>>>
```
</details>