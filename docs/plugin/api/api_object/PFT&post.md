<details> <summary>post and PFT: example code and use</summary>

```python
def main(api: dict, command_context: dict, plugin_space: dict):
    data = api["data"] 
    post = api["post"] # print error and register error
    PFT =  api["PFT"] # print formated text
    if len(command_context["command_arg"]) > 1:
        error = command_context["command_arg"][1]
    else:
        error = "test error"
    post(
        error, # any text 
        data 
    )
    PFT(
        data.last_error, # last error(post register error)
        data
    )
    """
    post signature - post(e: Any, data: Data)
    PFT signature - PFT(text: Any, data: Data)
    """
```

```pycon
>>> _pyt-eval_ data.last_error

>>> _#_ settings.md["shlex"] == True = True
>>> _example_plugin_
test error

test error

>>> _#_ settings.md["repl_mode"] == "globals" = True
>>> _pyt-eval_ data.last_error
test error

>>>
```

</details>