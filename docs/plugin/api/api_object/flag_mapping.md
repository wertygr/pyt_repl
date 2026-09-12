<details> <summary> signature: </summary>

```python
def flag_mapping(
        flag_map: dict[str, tuple[Callable, bool]], 
        command_args: list[str],
        *args,
        **kwargs) -> None:
    ...
```
</details>
<details> <summary> example: </summary>

```python
from plugins.plugin_tools.plugin_types import PluginApi, CommandContext

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    command_arg = command_context["command_arg"]
    flag_mapping = api["flag_mapping"]
    flag_map = {
        "test1": #flag 
            (
                lambda a: print(a, 1), #action
                True), # bool flag
        "test2": (lambda a: print(a, 2), False)
    }
    flag_mapping(flag_map, command_arg[1:], a="test: ")
```

```pycon
>>> _test_ test1 test2
test:  1
>>> _test_ test1
test:  1
test:  2
>>> _test_ test2
>>>
```
</details>

<details> <summary> truth table </summary>

| flag in command_args | bool flag | use action |
|:---------------------|:---------:|-----------:|
| True                 |   True    |       True |
| True                 |   False   |      False |
| False                |   True    |      False |
| False                |   False   |       True |

</details>

<details> <summary> read also </summary>

* [XNOR](https://en.wikipedia.org/wiki/XNOR_gate) 
</details>