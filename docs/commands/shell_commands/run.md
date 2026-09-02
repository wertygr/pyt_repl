syntax
```text
_._ run <path>
 ^   ^    ^
 |   |    |_ path for file
 |   |______ command
 |__________ prefix
```

example:
```pycon
>>> _sh_ cat other/script.pyre
_pyt-exec_ print("start test script")
_pyt-exec_ test_var = (5**85)*2
_pyt-eval_ test_var
_pyt-exec_ print("end test script")
>>> _._ run other/script.pyre
start test script
516987882845642296794630432543726783478632569313049316406250

end test script
>>>
```

<details> <summary> algorithm </summary>

- read lines for &lt;path>
- code: 

```python
for i in lines:
    if not lines[i]:
        continue
    data.command = lines[i]
    data.api["pars_command"](data)
```

</details>

<details> <summary> read also </summary>

[api](../../plugin/api/api.md)\
[api["pars_command"]](../../plugin/api/api_object/pars_command.md)

</details>