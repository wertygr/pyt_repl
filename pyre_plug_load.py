import importlib.util
import os
import sys
from typing import Optional, Any

from pyre_core import (
    PFT,
    Data,
    post,
    traceback_format
)

def _plugin_load(plugin, f_locate):
    spec = importlib.util.spec_from_file_location(plugin, f_locate)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[plugin] = module
    return module

def _plugin_cache_load(plugin, plugin_settings):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if plugin_settings.get("cache", False) and plugin in sys.modules:
        module = sys.modules[plugin]
    else:
        sys.modules.pop(plugin, None)
        file_name = plugin_settings.get("file", None)
        module = _plugin_load(plugin, f"{script_dir}/plugins/{file_name}")
    return module

def load_plugin(data: Data, plugin: Optional[str] = None) -> None:
    api = data.api
    if not plugin:
        plugin = data.command_arg[0]
    name_space = data.repl_mode

    plugin_settings = data.settings.get("plugin", {}).get(plugin, {})

    try:
        module = _plugin_cache_load(plugin, plugin_settings)

        name_space[plugin] = module
        module.main (api=api if plugin_settings.get("api", False) else {}, command_context={
            "command_arg": data.command_arg,
            "command_arg_int": data.command_arg_int,
            "command_prefix": data.command_prefix
        }, plugin_space=data.plugin_space)
    except Exception as e:
        post(e, data)

def unload_plugin(plugin_name, data):
    in_sys = plugin_name in sys.modules
    in_repl = plugin_name in data.repl_mode

    if not in_sys and not in_repl:
        e = f"[unload_plugin] plugin {plugin_name} not found anywhere"
        post(e, data)
        return

    if in_repl:
        del data.repl_mode[plugin_name]
    if in_sys:
        module = sys.modules[plugin_name]
        if hasattr(module, "destructor"):
            try:
                module.destructor(plugin_space=data.plugin_space)
            except Exception as e:
                post(e, data)
        del sys.modules[plugin_name]

def hooks_dispatch(data: Data, hook_name: str, hook_parameter: dict) -> list[Any]:
    api = data.api
    name_space = data.repl_mode
    result = []
    for i in data.settings["plugin"]:
        if not hook_name in data.settings["plugin"][i].get("hooks", []):
            continue
        plugin_settings = data.settings["plugin"][i]
        try:
            module = _plugin_cache_load(i, plugin_settings)
            name_space[i] = module
            result_plug_load = module.hook_run(
                api=api if plugin_settings.get("api", False) else {} ,
                hook=hook_name,
                hook_parameter=hook_parameter,
                plugin_space=data.plugin_space
            )
            result.append(result_plug_load)
        except Exception as e:
            if hook_name not in ("post", "PFT"):
                post(e, data)
                continue
            e = traceback_format(e)
            data.last_error = e
            PFT(e, data, use_hook=False)
            result.append(e)
    return result