<details> <summary> load </summary>
plugins are loaded in [data.repl_mode](api/api_object/data/repl_mode.md) and sys.moduls
</details>
<details> <summary> error in plugin </summary>

```python
def main(api: dict, command_context: dict, plugin_space: dict) -> None:
    bad_var = 0/0
```

```pycon
>>> _bad_plugin_
Traceback (most recent call last):
  File "/home/wertygr/PycharmProjects/SS/flash/pyre_plug_load.py", line 44, in _plugin
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
  File "/home/wertygr/PycharmProjects/SS/flash/plugins/bad_plugin.py", line 2, in main
    bad_var = 0/0
              ~^~
ZeroDivisionError: division by zero

>>>
```

</details>