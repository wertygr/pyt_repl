This command allows you to artificially call arbitrary hooks

syntax:
```text
_._ hook_run <name> <parameter>
 ^      ^       ^       ^
 |      |       |       |_ parameter
 |      |       |_________ hook name
 |      |_________________ command
 |________________________ prefix
```

example:
```pycon
>>> _#_ settings["shlex"] == True = true
>>> _._ hook_run "post" '{"err": "test error"}'
>>>
```

<details> <summary> read also </summary>

[hook](../../plugin/hook/hook.md)
[hook_dispatch](../../plugin/api/api_object/hook_dispatch.md)
</details>