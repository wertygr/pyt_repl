<details> <summary> load </summary>

plugins are loaded in [data.repl_mode](api/api_object/data/repl_mode.md) and sys.modules
</details>

<details> <summary> sandbox </summary>
there is no sandbox
</details>

<details> <summary> open file and import in plugin </summary>
Plugins open files and import modules relative to the project root

import: \
wrong
```python
import test
```
correct
```python
import plugins.test as test
```
</details>

<details> <summary> error in plugin </summary>

```python
from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict) -> None:
    bad_var = 0 / 0
```

```pycon
>>> _bad_plugin_
Traceback (most recent call last):
  File ".../pyre_plug_load.py", line 45, in load_plugin
    module.main (api=api if plugin_settings.get("api", False) else {}, command_context={
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "argv": data.argv,
        ^^^^^^^^^^^^^^^^^^
        "argc": data.argc,
        ^^^^^^^^^^^^^^^^^^
        "postfix": data.postfix
        ^^^^^^^^^^^^^^^^^^^^^^^
    }, plugin_space=data.plugin_space)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../plugins/test.py", line 4, in main
    bad_var = 0 / 0
              ~~^~~
ZeroDivisionError: division by zero

>>>
```

</details>

<details> <summary> unload plugin </summary>
unload from:

- the [destructor](plugin_destructor.md) is called
- [data.repl_mode](api/api_object/data/repl_mode.md)
- sys.modules

</details> 