<details> <summary> pars_command </summary> 

```python
from plugins.plugin_tools.types import (PluginData, PluginApi, CommandContext)

import time
def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    data = api["data"]
    PFT = api["PFT"]
    parser = api["pars_command"]
    cmd = command_context["command_prefix"]
    start_time = time.perf_counter()
    data.command = cmd
    parser(data)
    end_time = time.perf_counter()
    PFT(end_time - start_time, data)
```

```pycon
>>> _timer_ _pyt-exec_ import time; time.sleep(5)
5.0004651109920815

>>>
```

</details>