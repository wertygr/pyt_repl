import importlib.util
import os
import sys
from typing import Optional, Any

from pyre_core import PFT, Data
from pyre_core import post

def _plugin_load(plugin, f_locate):
    spec = importlib.util.spec_from_file_location(plugin, f_locate)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[plugin] = module
    return module

def _plugin_cache_load(plugin, plugin_settings):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if plugin_settings.get("cache", False) == True and plugin in sys.modules:
        module = sys.modules[plugin]
    else:
        sys.modules.pop(plugin, None)

        file_name = plugin_settings.get("file", None)
        module = _plugin_load(plugin, f"{script_dir}/plugins/{file_name}.py")
    return module

def _plugin(data: Data, plugin: Optional[str] = None) -> None:
    api = data.api
    if not plugin:
        plugin = data.command_arg[0]
    command_arg_int = data.command_arg_int
    command_arg = data.command_arg
    command_prefix = data.command_prefix
    name_space = data.repl_mode

    plugin_settings = api["settings"].get("plugin", {}).get(plugin, {})

    try:
        module = _plugin_cache_load(plugin, plugin_settings)

        name_space[plugin] = module
        result_plug_load = module.main (api=api, command_context={
            "command_arg": command_arg,
            "command_arg_int": command_arg_int,
            "command_prefix": command_prefix
        })
        if not(isinstance(result_plug_load, dict)):
            e = f"[_plugin]: invalid plugin result. plugin result = {result_plug_load}"
            post(e, data)
            return
        data.plugin_space[plugin] = result_plug_load
        return

    except Exception as e:
        post(e, data)

def unload_plugin(plugin_name, data):
    in_sys = plugin_name in sys.modules
    in_repl = plugin_name in data.repl_mode
    in_plugin_space = plugin_name in data.plugin_space

    if ((not(in_sys)) and (not(in_repl)) and (not(in_plugin_space))):
        e = f"[unload_plugin] plugin {plugin_name} not found anywhere"
        post(e, data)
        return

    if in_repl:
        del data.repl_mode[plugin_name]
    if in_sys:
        del sys.modules[plugin_name]
    if in_plugin_space:
        del data.plugin_space[plugin_name]

def hooks_dispatch(data: Data, hook_name: str, hook_parameter: dict):
    def _post(e: Any, data: Data) -> None:
        data.last_error = e
        PFT(f"{e}", data)
    api = data.api
    data.hook = hook_name
    name_space = data.repl_mode
    plugin_list = []
    for i in data.settings["plugin"]:
        if hook_name in data.settings["plugin"][i].get("hooks", []):
            plugin_list.append(i)
    for i in plugin_list:
        plugin_settings = data.settings["plugin"][i]
        try:
            module = _plugin_cache_load(i, plugin_settings)

            name_space[i] = module
            result_plug_load = module.hook_run(api=api, hook=hook_name, hook_parameter=hook_parameter)
            if not (isinstance(result_plug_load, dict)):
                e = f"[hooks_dispatch]: invalid type({type, result_plug_load}) plugin result. plugin result = {result_plug_load}"
                _post(e, data)
                continue
            data.plugin_space[i] = result_plug_load
        except Exception as e:
            _post(e, data)