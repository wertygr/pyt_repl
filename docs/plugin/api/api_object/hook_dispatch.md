Plugins can call hooks via the API.

<details> <summary> example code</summary> 

```python
def main(api: dict, command_context: dict, plugin_space: dict):
    hooks_dispatch = api["hook_dispatch"]
    data = api["data"]
    hook_parametr = {}
    hooks_dispatch(data, "hook_name", hook_parametr)
```

</details>