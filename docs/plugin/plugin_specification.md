<details> <summary> load </summary>

plugins are loaded in [data.repl_mode](api/api_object/data/repl_mode.md) and sys.modules
</details>

<details> <summary> sandbox </summary>
there is no sandbox
</details>

<details> <summary> open file in plugin </summary>
Plugins open files relative to the project root
</details>

<details> <summary> error in plugin </summary>

```python
def main(api: dict, command_context: dict, plugin_space: dict) -> None:
    bad_var = 0/0
```

```pycon
>>> _bad_plugin_
Traceback (most recent call last):
  File ".../pyre_plug_load.py", line 44, in _plugin
    module.main (api=api, command_context={
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "command_arg": command_arg,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "command_arg_int": command_arg_int,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "command_prefix": command_prefix
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    }, plugin_space=data.plugin_space)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../plugins/bad_plugin.py", line 2, in main
    bad_var = 0/0
              ~^~
ZeroDivisionError: division by zero

>>>
```

</details>

<details> <summary> unload plugin </summary>
unload from:

- sys.modules
- [data.repl_mode](api/api_object/data/repl_mode.md)
- data.plugin_space[plugin_name]
</details> 