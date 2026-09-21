<details> <summary> signature </summary>

```python
def pft(text: Any, data: Data, end: str= "\n", use_hook: bool = True, file:TextIO = sys.stdout) -> None:
    ...
```
</details>

<details> <summary> example </summary>

```python
from plugins.plugin_tools.plugin_types import (PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    data = api["data"]
    pft = api["pft"]  # print formated text(with syntax highlighting(python3))
    pft(
        """
class test:
    def __init__(self):
        self.a = 1
        self.b = 0        
        """,  # text
        data
    )
    """
    def PFT(text: str, data: Data, end: str= "\n") -> None:
    """
```
```pycon
>>> _test_
class test:
    def __init__(self):
        self.a = 1
        self.b = 0


>>>
```

![example_pft.png](../../../img/example_pft.png)
</details>