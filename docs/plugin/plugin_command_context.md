command_context this is dict[str, str|int|list[str]]

<details> <summary> example </summary>


```python
from plugins.plugin_tools.plugin_types import CommandContext, PluginApi
def main(api: PluginApi, command_context: CommandContext, plugin_space: dict): 
    print(command_context)
```

```pycon
>>> _test_
{'argv': ['_test_'], 'argc': 1, 'postfix': ''}
>>> _test_ f f f 1 2 3 4 5
{'argv': ['_test_', 'f', 'f', 'f', '1', '2', '3', '4', '5'], 'argc': 9, 'postfix': 'f f f 1 2 3 4 5'}
>>> _test_ "1 2 3 4"
{'argv': ['_test_', '"1', '2', '3', '4"'], 'argc': 5, 'postfix': '"1 2 3 4"'}
>>> _#_ settings["shlex"] == True = False
>>> _._ settings_reload
>>> _test_ "1 2 3 4"
{'argv': ['_test_', '1 2 3 4'], 'argc': 2, 'postfix': '1 2 3 4'}
>>> _#_ settings["shlex"] == True = True && settings["posix"] == True = True
>>>
```

</details>

<details> <summary> objects </summary>

| name    | type      |                           description |
|:--------|-----------|--------------------------------------:|
| argc    | int       |                 size args in commands |
| arhv    | list[str] |                                  args |
| postfix | str       |  the entire line after the first word |
</details>

<details> <summary> read also </summary>

[pipeline](../commands/pipeline.md)
</details>