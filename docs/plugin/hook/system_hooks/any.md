A meta-hook that allows you to react to absolutely any hook without explicitly specifying it.

<details> <summary> example </summary>

```json
{
    "plugin": {
        "_test_": {
            "file": "test.py",
            "cache": true,
            "api": true,
            "hooks": ["__any__"]
        }
    }
}
```
```python
from plugins.plugin_tools.plugin_types import PluginApi

def hook_run(api: PluginApi, hook: str, hook_parameter: dict, plugin_space: dict):
    print(f"name_name: {hook}\nhook_parameter: {hook_parameter}")
```
```pycon
name_name: init
hook_parameter: {'data': <pyre_core.Data object at 0x7f1017ae6e40>}
>>> _pyt-eval_ 5+5
10

name_name: pft
hook_parameter: {'text': '10'}
>>> _pyt-eval_ 5/0
name_name: post
hook_parameter: {'err': 'Traceback (most recent call last):\n  File ".../pyre_commands.py", line 104, in pyt_eval\n    pft(eval(data.postfix, data.repl_mode), data)\n        ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "<string>", line 1, in <module>\nZeroDivisionError: division by zero\n'}
Traceback (most recent call last):
  File ".../pyre_commands.py", line 104, in pyt_eval
    pft(eval(data.postfix, data.repl_mode), data)
        ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 1, in <module>
ZeroDivisionError: division by zero

name_name: pft
hook_parameter: {'text': 'Traceback (most recent call last):\n  File ".../pyre_commands.py", line 104, in pyt_eval\n    pft(eval(data.postfix, data.repl_mode), data)\n        ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "<string>", line 1, in <module>\nZeroDivisionError: division by zero\n'}
```

</details>