<details> <summary>buffer: example code and use</summary>

```python
def main(api: dict, command_context: dict, plugin_space: dict):
    buffer = api["buffer"]
    """
    arg_1 - mode(type str) "copy"/"paste"/"add"
    arg_2 - text(type str)
    
    buffer signature - buffer(mode: str, text: str)
    
    mode="copy" - read buffer
    mode="add" - add to buffer
    mode="paste" - paste to buffer
    """
    print(buffer("copy"))
```
example use:
```pycon
>>> _#_ settings.md["repl_mode"] == "globals" = True
>>> _?_ buffer -copy -silent
>>> _example-plugin_
def buffer (mode: str = "copy", text: str = ""):
    global _buffer
    if mode == "copy":
        return _buffer
    if mode == "paste":
        _buffer = text
    elif mode == "add":
        _buffer += text

>>>
```

</details>