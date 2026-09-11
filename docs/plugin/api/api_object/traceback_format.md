<details> <summary> signature: </summary>

```python
def traceback_format(e: TracebackType|BaseException|str) -> str:
    ...
```
</details>>

<details> <summary> example: </summary>

```python
from plugins.plugin_tools.plugin_types import PluginApi, CommandContext

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    traceback_format = api["traceback_format"]
    try:
        bad_var = 0/0
    except ZeroDivisionError as e:
        with open("test_error.txt", "w") as f:
            f.write(traceback_format(e))
```
```pycon
>>> _test_
>>> ! cat test_error.txt
Traceback (most recent call last):
  File ".../plugins/test.py", line 6, in main
    bad_var = 0/0
              ~^~
ZeroDivisionError: division by zero
>>>
```
</details>