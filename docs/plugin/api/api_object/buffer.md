```python
from plugins.plugin_tools.plugin_types import (PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    buffer = api["buffer"]
    data = api["data"]
    """
    arg_0 - data
    arg_1 - mode(type str) "write"/"write_add"/"read"
    arg_2 - Optional[text(type str)]
    
    buffer signature - buffer(mode: str, text: str)
    
    mode="read"  - read buffer
    mode="write_aad"   - add to buffer
    mode="write" - write to buffer
    """
    print(buffer(data, "read"))
```
example use:
```pycon
>>> _#_ settings["shlex"] == True = True
>>> _._ buffer write "0 1 2 3 4 5 6 7 8 9"
>>> _test_
0 1 2 3 4 5 6 7 8 9
>>>
```