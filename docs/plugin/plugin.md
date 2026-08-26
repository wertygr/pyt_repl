**plugins:**

<details> <summary>contract</summary>

plugin - this is file in folder "./plugins" with main function\
the "main" function must return a Any(ignore)\
the "main" function must take 2 parameters:

- 1 API: dict,
- 2 command_context: dict 
- 3 plugin_space: dict

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
            "file": "plug_test",
            "cache": true,
            "api": true
        } 
    }
}
```
</details>

| name           | type |                                             description |
|:---------------|------|--------------------------------------------------------:|
| \_test_plugin_ | str  |                                             plugin name |
| file           | str  | file name(in folder: "plugins"(without file extension)) |
| api            | bool |                                            use pyre api |
| cache          | bool |                                  use cache(sys.modules) |

<details> <summary>example plugin code</summary>

```python
# code in ./plugins/plug_test
def main(api: dict, command_context: dict, plugin_space: dict):
    for i in command_context:
        print(f"{i}: {command_context[i]}")
```
</details>

<details> <summary>example use plugin</summary>

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
</details>

unload plugin: 
```commandline
_._ unload_plug <plugin_name>
```
***
* [plugin api](api/api.md)