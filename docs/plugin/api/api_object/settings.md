<details> <summary>settings: example code and use</summary>

```python
def main(api: dict, command_context: dict, plugin_space):
    if len(command_context["command_arg"]) < 2:
        new_prompt = ">>>> "
    else:
        new_prompt = command_context["command_arg"][1]
    api["settings.md"]["prompt"] = new_prompt
```

```pycon
>>> _#_ settings.md["shlex"] == True = True
>>> _example_plugin_ :>>>
:>>>_example_plugin_ ":>>> "
:>>> _example_plugin_ ">>> "
>>> _example_plugin_
>>>>
```
</details>