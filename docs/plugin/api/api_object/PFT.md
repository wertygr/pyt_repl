```python
from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)


def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    data = api["data"]
    pft = api["PFT"]  # print formated text(with syntax highlighting(python3))
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

![example_PFT.png](../../../img/example_pft.png)