python repl
***
**install:**
```bash
mkdir pyrepl
cd pyrepl
git clone <repo-url>
pip install req.txt
python pyre.py
```
***
**fast start:**
```pycon
>>> _pyt-exec_ var = "test var"
>>> _pyt-eval_ var
test var

>>> _pyt-exec_ def test_function(): pass
>>> _?_ test_function
def test_function(): pass

>>> _?_ test_function -copy -silent
>>> _pyt++_ paste
1 |def test_function():
  2 |     pass # this is multiline editor
  3 |
  4 |# Esp + Enter = exit and execute code
  5 |# Ctrl + c = exit
>>> _?_ test_function
def test_function():
     pass # this is multiline editor

>>> _pyt-exec_ g = 55 _&_ _pyt-eval_ g _&_ _?_ g
55

g = 55

>>> _#_ comment
>>> _sh_ ls /
bin  boot  dev	etc  home  lib	lib64  lost+found  mnt	opt  proc  root  run  sbin  srv  swapfile  sys	tmp  usr  var
>>> _pyt_ print(
--------------- 
eval: '(' was never closed (<py_repl_5>, line 1) 
---------------
exec: '(' was never closed (<py_repl_5>, line 1) 
---------------

>>> _pyt_ import time
>>> _pyt_ (2+88)**5
5904900000

>>> _pyt_ print(
__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ 
eval: '(' was never closed (<py_repl_7>, line 1) 
__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ 
exec: '(' was never closed (<py_repl_7>, line 1) 
__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ 

>>> _._ exit

```
***
| prefix                         |          arg           |                    info |
|:-------------------------------|:----------------------:|------------------------:|
| \_?_                           |   \<object> \<flag>    |           introspection |
| \_pyt++_                       |        \<flag>         |        multiline editor |
| \_pyt-exec_                    |        \<code>         |            execute code |
| \_pyt-eval_                    |        \<code>         |               eval code |
| \_._                           | \<command> \<argument> |            repl command |
| \_#_                           |       \<comment>       |                 comment |
| \<command_1> \_&_ \<command_2> |                        |                pipeline |
| \_sh_                          |       \<command>       | command on system shell |
| \_pyt_                         |        \<code>         |      auto(eval or exec) |
***
**req:**\
python3.12+(test on 3.14.6)\
python-jedi\
python-prompt-toolkit\
python-pygments\
python-tabulate
***
**settings:**\
The settings are located in the file: "./.pyre_settings.json"(parsing for std lib python "json")
<details> <summary>example settings</summary>

```json
{
    "color": {
        "Whitespace": "#cccccc",
        "Comment": "italic #7A7E85",
        "Comment.Preproc": "bold #CF8E6D",
        "Keyword": "bold #CF8E6D",
        "Keyword.Declaration": "bold #CF8E6D",
        "Name.Function": "#56A8F5",
        "String": "#6AAB73",
        "Operator": "#cccccc",
        "Literal.Number": "#2AACB8",
        "Name.Builtin": "#8888C6",
        "Operator.Word": "#CF8E6D",
        "Literal.String.Interpol": "#CF8E6D",
        "Name.Exception": "#8888C6",
        "Literal.String.Escape": "#CF8E6D",
        "Name.Function.Magic": "#B200B2",
        "Name.Builtin.Pseudo": "#94558D",
        "Name.Namespace": "#cccccc",
        "Name": "#cccccc",
        "Name.Decorator": "#B3AE60",
        "Name.Variable.Magic": "#cccccc",
        "Name.Class": "#cccccc"
    },
    "line_name_format": "{line_number:>{width}} |",
    "prompt": ">>> ",
    "plugin": {},
    "separator": true,
    "repl_mode": "globals",
    "shell_container": true,
    "shlex": true,
    "multiline": false,
    "alias_globals": true,
    "alias_locals": true,
    "posix": true,
    "alias_dict": {
        "example_alias": {
            "scope": "local",
            "value": ["_pyt-exec_", "print(2+2)"],
            "position": [0] 
        },
        ";;": {
            "scope": "global",
            "value": ["_&_"],
            "position": null 
        }
    }
}
```
</details>


| name                           | type |                                                                                                                                  description |
|:-------------------------------|:----:|---------------------------------------------------------------------------------------------------------------------------------------------:|
| prompt                         | str  |                                                                                                                                       prompt |
| color                          | dict |                                                                                                   syntax highlighting(format prompt-toolkit) |
| line_name_format               | str  |                                                                                                       format number line in multiline editor |
| shlex                          | bool |                                                                                                                use shlex for command parsing |
| posix                          | bool |                                                                                                    use posix for parsing command(with shlex) |
| multiline                      | bool |                                                                                                                                use multiline |
| separator                      | bool |                                                                                                                           use pipeline(\_&_) |
| repl_mode                      | str  |   if data.settings.get("repl_mode")== "globals":<br/>repl_mode = globals()<br/> else: repl_mode = data.local_repl_mode <br/>#repl name space |
| alias_globals<br/>alias_locals | bool |                                                                                                                                    use alias |
| alias_dict                     | dict |                                                                                                                                 regist alias |
| plugin                         | dict |                                                                                                                                regist plugin |
| shell_container                | bool |                                  integration system shell & pyre<br/> example:<br/>>>> \_pyt-exec_ fffff = 4<br/>>>> \_sh_ echo $fffff<br/>4 |
***

**plugins:**

<details> <summary>contract</summary>
plugin - this is file in folder "./plugins" with main function 
the "main" function must return a dict
the "main" function must take 2 parameters:
    1 API: dict,
    2 command_context: dict 

```python
def main(api: dict, command_context: dict) -> dict:
    return {} # minimal plugin code
```

</details>

register plugin(in settings):
<details> <summary>example settings plugin</summary>

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
def main(api: dict, command_context: dict) -> dict:
    for i in command_context:
        print(f"{i}: {command_context[i]}")
    return {} # the "main" function must return a dict
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
**plugin API:**

<details> <summary>buffer: example code and use</summary>

```python
def main(api: dict, command_context: dict) -> dict:
    buffer = api["buffer"]
    """
    arg_1 - mode(type str) "copy"/"paste"/"add"
    arg_2 - text(type str)
    
    mode "copy" - read buffer
    mode "add" - add to buffer
    mode "paste" - paste to buffer
    """
    print(buffer("copy"))
    return {}
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
def main(api: dict, command_context: dict) -> dict:
    if len(command_context["command_arg"]) < 2:
        new_prompt = ">>>> "
    else:
        new_prompt = command_context["command_arg"][1]
    api["settings"]["prompt"] = new_prompt
    return {}
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
def main(api: dict, command_context: dict) -> dict:
    register_repl_source = api["register_repl_source"]
    data = api["data"]
    code = """
def test():
    pass
    """
    f_name = register_repl_source(code, data)
    exec(compile(code, f_name, "exec"), data.repl_mode)
    return {}
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

_(doc in work)_
***