import importlib.util
import json
import os
import sys
import ast

from tabulate import tabulate

from simple_shell_core import PFT
from simple_shell_core import post

err = "\033[31m"
bs = "\033[0m"

def plugin_ss(data) -> None:
    ss_api = data.ss_api
    plugin = data.command_arg[0]
    command_arg_int = data.command_arg_int
    command_arg = data.command_arg
    command_prefix = data.command_prefix
    name_space = data.repl_mode
    script_dir = data.script_dir

    plugin_settings = ss_api["settings"].get("plugin", {}).get(plugin, {})

    try:
        if plugin_settings.get("cache", False) == True and plugin in sys.modules:
            module = sys.modules[plugin]
        else:
            sys.modules.pop(plugin, None)

            file_name = plugin_settings.get("file", None)
            if not(file_name):
                return
            spec = importlib.util.spec_from_file_location(
                plugin,f"{script_dir}/plugins_ss/{file_name}.py")

            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin] = module
            spec.loader.exec_module(module)

        if plugin_settings.get("ss_api", False) == True:
            module.ss_api = ss_api

        else:
            module.main_globals = {}
        name_space[plugin] = module
        result_plug_load = module.main(ss_api=ss_api, command_context={
            "command_arg": command_arg,
            "command_arg_int": command_arg_int,
            "command_prefix": command_prefix
        })
        if not(isinstance(result_plug_load, dict)):
            e = f"[plugin_ss]: invalid plugin result. plugin result = {result_plug_load}"
            post(e, data)
            return
        data.plugin_space[data.command_arg[0]] = result_plug_load
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

def plugins_list(data):
    script_dir = data.script_dir
    def check_dispatch(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                tree = ast.parse(file.read())

            for i in ast.walk(tree):
                if isinstance(i, ast.FunctionDef) and i.name == "main":
                    return True
        except Exception as e:
            post(e, data)
        return False
    try:
        with open(f"{script_dir}/.simple_shell_settings.json") as f:
            settings = json.load(f)
        table_data = []

        for i in settings.get("plugin", {}):
            plugin_info = settings["plugin"][i]
            filename = plugin_info.get("file", "None")

            plugin_file = f"{filename}.py"
            full_path = f"{script_dir}/plugins_ss/{plugin_file}"

            if os.path.isfile(full_path):
                func = check_dispatch(full_path)
                table_data.append([i, plugin_file, str(func)])

        headers = ["prefix", "file_Name", "main"]

        PFT(tabulate(table_data, headers=headers, tablefmt="grid"), data)
    except FileNotFoundError as e:
        post(e, data)
    except Exception as e:
        post(e, data)