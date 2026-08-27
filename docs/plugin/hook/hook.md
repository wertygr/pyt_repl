<details> <summary> contact </summary> 

plugin - this is file in folder "./plugins" "with hook_run" function\
the "hook_run" function must return an Any\
the "hook_run" function must take 3 parameters(kwargs):

- 1 API: dict,
- 2 hook: str, 
- 3 hook_parameter: dict

```python
def hook_run(api: dict, hook: str, hook_parameter: dict):
    return
```

</details>

<details> <summary> plugin register in settings </summary> 

```json
{
    "plugin": {
        "_example_": {
            "file": "example.py",
            "cache": true,
            "api": true,
            "hooks": ["post"]
        }
    }
}
```

</details>

<details> <summary> example code </summary> 

```python
def hook_run(api: dict, hook: str, hook_parameter: dict):
    data = api["data"]
    post = api["post"]
    if hook != "post":
        e = f"[logger::hook_run]: This hook is not supported: {hook}"
        post(e, data)
        return
    with open("err_log", "a") as f:
        f.write(f"{hook_parameter['err']}\n")
```
This Python code use system hooks "post" 
</details>

* [description for system hooks](system_hooks.md)
* [plugin create hooks](../api/hook_dispath.md)