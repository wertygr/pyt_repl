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