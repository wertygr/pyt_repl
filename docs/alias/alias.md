alias:

<details> <summary> example alias </summary>:

```json
{
    "alias_dict": {
        "!": {
            "scope": "local",
            "position": [0],
            "value": ["_sh_"]
        }
    }
}
```

| name     |      type       |                                                                                        description |
|:---------|:---------------:|---------------------------------------------------------------------------------------------------:|
| !        |       str       |                                                                                         name alias |
| scope    |       str       |                                                                                        scope alias |
| positoin | list[int]\|null |  A parameter specifying where the macro will be placed; if set to "None", it is applied everywhere |
| value    |    list[str]    |                                                                                        value alias |
</details>

<details> <summary> scope </summary>

| scope  |                                        description |
|:-------|---------------------------------------------------:|
| global |  processed up to the "command_separator" delimiter |
| local  |  processed after the "command_separator" delimiter | 
</details>

<details> <summary> parsing token and alias:</summary>
<details> <summary> aliases from the example: </summary>

```json
{
    "alias_dict": {
        "!": {
            "scope": "locals",
            "position": [0],
            "value": ["_sh_"]
        },
        "pyt-ev": {
            "scope": "locals",
            "position": [0],
            "value": ["_pyt-eval_"]
        },
        ";;": {
            "scope": "global",
            "position": null,
            "value": ["_&_"]
        }
    }
}
```
</details>

parsing:
```text
command:
"! ls / ;; _pyt-eval_ 5+5"

after breaking it down into arguments:
["!", "ls", "/", ";;", "pyt-ev", "5+5"]

after global alias substitution:
["!", "ls", "/", "_&_", "pyt-ev", "5+5"]

after splitting into sub-teams:
[["!", "ls", "/"], ["pyt-ev", "5+5"]]

after global alias substitution:
[["_sh_", "ls", "/"], ["_pyt-eval_", "5+5"]]
```
</details>

<details> <summary> macros </summary>
N - number

| syntax |      descripion |
|:-------|----------------:|
| \>#N   |  relative shift |
| !#N    |  absolute index |
</details>