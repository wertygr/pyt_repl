**plugins:**

<details> <summary>Warning</summary>
plugins do not have a sandbox!!!
</details>

<details> <summary>contract</summary>

Plugin - this is file in folder "./plugins" with main function\
The "main" function can return Any (the return value is ignored).
The "main" function must take 3 parameters(kwargs):

- 1 API: dict,
- 2 command_context: dict 
- 3 plugin_space: dict

plugins are loaded via [importlib](https://docs.python.org/3/library/importlib.html)

```python
from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)


def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    pass
```

</details>

<details> <summary>register plugin(in settings): example settings plugin</summary>

```json
{
    "plugin": {
        "_test_": {
            "file": "plug_test.py",
            "cache": true,
            "api": true
        } 
    }
}
```

| name    | type |                      description |
|:--------|------|---------------------------------:|
| \_test_ | str  |                      plugin name |
| file    | str  | file name(in folder: "plugins" ) |
| api     | bool |                     use pyre api |
| cache   | bool |           use cache(sys.modules) |
</details>

<details> <summary>example plugin code</summary>

code:

```python
# code in ./plugins/plug_test

from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)


def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    for i in command_context:
        print(f"{i}: {command_context[i]}")
```

use:
```pycon
>>> _test_ test plugin
argv: ['_test_', 'test', 'plugin']
argc: 3
postfix: test plugin
>>> _test_ test plugin 1 2 3 4 5 6 7 8 9 0
argv: ['_test_', 'test', 'plugin', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
argc: 13
postfix: test plugin 1 2 3 4 5 6 7 8 9 0
>>>
```

unload plugin: 
```pycon
>>> _._ unload_plug <plugin_name>
```

</details>

***
<details> <summary> read also</summary>

* [plugin_space](plugin_space.md)
* [plugin api](api/api.md)
* [hooks](hook/hook.md)
* [plugin specification](plugin_specification.md)
* [plugin type](plugin_types.md)
</details>