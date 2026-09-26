<details> <summary> load </summary>

plugins are loaded in [data.repl_mode](api/api_object/data/repl_mode.md) and sys.modules
</details>

<details> <summary> sandbox </summary>
there is no sandbox
</details>

<details> <summary> open file and import in plugin </summary>
Plugins open files and import modules relative to the project root

import: \
wrong
```python
import test
```
correct
```python
import plugins.test as test
```
</details>

<details> <summary> error in plugin </summary>

```python
from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict) -> None:
    bad_var = 0 / 0
```

```pycon
>>> _bad_plugin_
Traceback (most recent call last):
  File ".../pyre_plug_load.py", line 45, in load_plugin
    module.main (api=api if plugin_settings.get("api", False) else {}, command_context={
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        "argv": data.argv,
        ^^^^^^^^^^^^^^^^^^
        "argc": data.argc,
        ^^^^^^^^^^^^^^^^^^
        "postfix": data.postfix
        ^^^^^^^^^^^^^^^^^^^^^^^
    }, plugin_space=data.plugin_space)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../plugins/test.py", line 4, in main
    bad_var = 0 / 0
              ~~^~~
ZeroDivisionError: division by zero

>>>
```

</details>

<details> <summary> hook recursion </summary>
If the plugin crashes, its traceback is output via "post"; however, if the plugin was subscribed to any of {"post", "pft", "__any__"}, 
then "post" is called with the flag `use_hook = False` to avoid recursion.

If a plugin triggers a hook (via ["hooks_dispatch"](api/api_object/hook_dispatch.md)) that it is itself subscribed to, this leads to recursion.
<details> <summary> example </summary>

```python
from plugins.plugin_tools.plugin_types import (PluginData, PluginApi, CommandContext)

def hook_run(api: PluginApi, hook: str, hook_parameter: dict, plugin_space: dict):
    hooks_dispatch = api["hook_dispatch"]
    data = api["data"]
    hooks_dispatch(data, "bad_hook", {})

def main(api: PluginApi, command_context: CommandContext, plugin_space: dict):
    hooks_dispatch = api["hook_dispatch"]
    data = api["data"]
    hooks_dispatch(data, "bad_hook", {})
```

```json
{
    "plugin": {
        "_bad_plug_": {
            "file": "bad_plug.py",
            "cache": true,
            "api": true,
            "hooks": ["bad_hook"]
        }
    }
}
```
```pycon
>>> _bad_plug_
Traceback (most recent call last):
  File ".../pyre_plug_load.py", line 76, in hooks_dispatch
    module = _plugin_cache_load(i, plugin_settings)
  File ".../pyre_plug_load.py", line 22, in _plugin_cache_load
    script_dir = os.path.dirname(os.path.abspath(__file__))
  File "<frozen posixpath>", line 179, in dirname
RecursionError: maximum recursion depth exceeded

During handling of the above exception, another exception occurred:

...
RecursionError: maximum recursion depth exceeded

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File ".../pyre_plug_load.py", line 78, in hooks_dispatch
    result_plug_load = module.hook_run(
        api=api if plugin_settings.get("api", False) else {} ,
    ...<2 lines>...
        plugin_space=data.plugin_space
    )
  File ".../bad_plug.py", line 6, in hook_run
    hooks_dispatch(data, "bad_hook", {})
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File ".../pyre_plug_load.py", line 87, in hooks_dispatch
    post(e, data, use_hook=False if hook_name in ("pft", "post", "__any__") else True)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../pyre_core.py", line 97, in post
    e = traceback_format(e)
  File ".../pyre_core.py", line 93, in traceback_format
    e = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/traceback.py", line 158, in format_exception
    te = TracebackException(type(value), value, tb, limit=limit, compact=True)
  File "/usr/lib/python3.14/traceback.py", line 1058, in __init__
    self.stack = StackSummary._extract_from_extended_frame_gen(
                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        _walk_tb_with_full_positions(exc_traceback),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        limit=limit, lookup_lines=lookup_lines,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        capture_locals=capture_locals)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/traceback.py", line 505, in _extract_from_extended_frame_gen
    f.line
  File "/usr/lib/python3.14/traceback.py", line 374, in line
    self._set_lines()
    ~~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.14/traceback.py", line 352, in _set_lines
    line = linecache.getline(self.filename, lineno).rstrip()
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/linecache.py", line 26, in getline
    lines = getlines(filename, module_globals)
  File "/usr/lib/python3.14/linecache.py", line 41, in getlines
    return updatecache(filename, module_globals)
  File "/usr/lib/python3.14/linecache.py", line 187, in updatecache
    with tokenize.open(fullname) as fp:
         ~~~~~~~~~~~~~^^^^^^^^^^
  File "/usr/lib/python3.14/tokenize.py", line 463, in open
    encoding, lines = detect_encoding(buffer.readline)
                      ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/tokenize.py", line 427, in detect_encoding
    first = read_or_stop()
RecursionError: maximum recursion depth exceeded
```
</details>
</details>

<details> <summary> unload plugin </summary>
unload from:

- the [destructor](plugin_destructor.md) is called
- [data.repl_mode](api/api_object/data/repl_mode.md)
- sys.modules

</details> 