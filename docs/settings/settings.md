**settings:**\
The settings are located in the file: "./.pyre_settings.json"(parsing for std lib python [json](https://docs.python.org/3/library/json.html))
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


<details> <summary> table </summary>

| name                            | type |                                                                                                                                description |
|:--------------------------------|:----:|-------------------------------------------------------------------------------------------------------------------------------------------:|
| prompt                          | str  |                                                                                                                                     prompt |
| color                           | dict |    syntax highlighting([format prompt-toolkit](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/advanced_topics/styling.html)) |
| line_name_format                | str  |                                                                                                     format number line in multiline editor |
| shlex                           | bool |                                                                                                              use shlex for command parsing |
| posix                           | bool |                                                                                                  use posix for parsing command(with shlex) |
| multiline                       | bool |                                                                                                                              use multiline |
| separator                       | bool |                                                                                                                         use pipeline(\_&_) |
| repl_mode                       | str  | if data.settings.get("repl_mode")== "globals":<br/>repl_mode = globals()<br/> else: repl_mode = data.local_repl_mode <br/>#repl name space |
| alias_globals<br/>alias_locals  | bool |                                                                                                                                  use alias |
| [alias_dict](../alias/alias.md) | dict |                                                                                                                               regist alias |
| plugin                          | dict |                                                                                                                              regist plugin |
| shell_container                 | bool |                                integration system shell & pyre<br/> example:<br/>>>> \_pyt-exec_ fffff = 4<br/>>>> \_sh_ echo $fffff<br/>4 |

</details>

***

* [default_settings](default_settings.md)

***