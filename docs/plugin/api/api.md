**plugin API:**

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
>>> _#_ settings["repl_mode"] == "globals" = True
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

<details> <summary>settings: example code and use</summary>

```python
def main(api: dict, command_context: dict, plugin_space):
    if len(command_context["command_arg"]) < 2:
        new_prompt = ">>>> "
    else:
        new_prompt = command_context["command_arg"][1]
    api["settings"]["prompt"] = new_prompt
```

```pycon
>>> _#_ settings["shlex"] == True = True
>>> _example_plugin_ :>>>
:>>>_example_plugin_ ":>>> "
:>>> _example_plugin_ ">>> "
>>> _example_plugin_
>>>>
```
</details>

<details> <summary>register_repl_source & data.repl_mode: example code and use</summary>
data this is an instance of a class "Data"
register_repl_source this is function in api used for source code registration and introspection

```python
def main(api: dict, command_context: dict, plugin_space: dict):
    register_repl_source = api["register_repl_source"]
    data = api["data"]
    code = """
def test():
    pass
    """
    f_name = register_repl_source(code, data)
    exec(compile(code, f_name, "exec"), data.repl_mode)
```

```pycon
>>> _?_ test
[source_code]: no object: test



>>> _example_plugin_
>>> _?_ test
def test():
    pass

>>>
```

</details>

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

>>> _#_ settings["shlex"] == True = True
>>> _example_plugin_
test error

test error

>>> _#_ settings["repl_mode"] == "globals" = True
>>> _pyt-eval_ data.last_error
test error

>>>
```

</details>

<details><summary>command_separator: example code and use</summary>

```python
def main(api: dict, command_context: dict, plugin_space: dict):
    post = api["post"]
    data = api["data"]
    command_separators = api["command_separators"]

    if command_context["command_arg_int"] < 2:
        post("[_example_plugin_::main]: not enough arguments", data)
        return {}
    commands = command_separators(command_context["command_arg"][1].split())
    print(f"command_arg: {command_context['command_arg']}\ncommands: {commands}\n__")
    for i in commands:
        print(i)
```

```pycon
>>> _#_ settings["shlex"] == True = True; settings["posix"] == True = True
>>> _example_plugin_ "command_1 _&_ command2 _&_ command3"
command_arg: ['_example_plugin_', 'command_1 _&_ command2 _&_ command3']
commands: [['command_1'], ['command2'], ['command3']]
__
['command_1']
['command2']
['command3']
>>>
```

</details>

_(doc in work)_

***