**plugins:**

<details> <summary>Warning</summary>
plugins do not have a sandbox!!!
</details>

<details> <summary>contract</summary>

plugin - this is file in folder "./plugins" with main function\
the "main" function must return an Any(ignore)\
the "main" function must take 3 parameters(kwargs):

- 1 API: dict,
- 2 command_context: dict 
- 3 plugin_space: dict

plugins are loaded via [importlib](https://docs.python.org/3/library/importlib.html)

```python
def main(api: dict, command_context: dict, plugin_space: dict):
    pass
```

</details>

<details> <summary>register plugin(in settings): example settings plugin</summary>

```json
{
    "plugin": {
        "_test_plugin_": {
            "file": "plug_test.py",
            "cache": true,
            "api": true
        } 
    }
}
```

| name           | type |                      description |
|:---------------|------|---------------------------------:|
| \_test_plugin_ | str  |                      plugin name |
| file           | str  | file name(in folder: "plugins" ) |
| api            | bool |                     use pyre api |
| cache          | bool |           use cache(sys.modules) |
</details>

<details> <summary>example plugin code</summary>

code:
```python
# code in ./plugins/plug_test
def main(api: dict, command_context: dict, plugin_space: dict):
    for i in command_context:
        print(f"{i}: {command_context[i]}")
```

use:
```pycon
>>> _test_plugin_ test plugin
command_arg: ['_test_plugin_', 'test', 'plugin']
command_arg_int: 3
command_prefix: test plugin
>>> _test_plugin_ test plugin 1 2 3 4 4
command_arg: ['_test_plugin_', 'test', 'plugin', '1', '2', '3', '4', '4']
command_arg_int: 8
command_prefix: test plugin 1 2 3 4 4
>>>
```

unload plugin: 
```pycon
>>> _._ unload_plug <plugin_name>
```

</details>

***
<details> <summary> read also</summary>

* [plugin api](api/api.md)
* [hooks](hook/hook.md)
* [plugin specification](plugin_specification.md)
* [plugin type](plugin_types.md)
</details>