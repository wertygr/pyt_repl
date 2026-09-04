example:

```python
PLUGIN_NAME = "_test_"

def main(api: dict, command_context: dict, plugin_space: dict):
    # init
    if PLUGIN_NAME not in plugin_space:
        plugin_space[PLUGIN_NAME] = {
            "i": 0
        }
    i = plugin_space[PLUGIN_NAME]["i"]
    print(i)
    plugin_space[PLUGIN_NAME]["i"] += 1
```

```pycon
>>> _test_
0
>>> _test_
1
>>> _test_
2
>>>
```