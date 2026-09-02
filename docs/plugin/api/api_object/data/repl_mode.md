data.repl_mode - user namespace

```python
# example use data.repl_mode 
def main(api: dict, command_context: dict, plugin_space: dict):
    data = api["data"]
    code = "# Any python code"
    exec(code, data.repl_mode) # it is recommended to register the source code 
```

<details> <summary> global/local(in settings "repl_mode") difference </summary>

locals - execution in an isolated namespace\
globals - execution in the kernel namespace

locals:
```pycon
>>> _?_ main
[source_code]: not object: main

>>>
```

globals:
```pycon
>>> _?_ main
def main() -> None:
    data = initialisation()
    repl_cycle(data)

>>>
```

</details>

<details> <summary> read also </summary>

[settings](../../../../settings/settings.md)\
[register_repl_source](../register_repl_source.md)

</details>