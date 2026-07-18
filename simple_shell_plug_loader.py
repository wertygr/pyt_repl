import importlib.util
import json
import os
import sys
import ast

from tabulate import tabulate

from simple_shell_core import PFT
from simple_shell_core import post

script_dir = os.path.dirname(__file__)
err = "\033[31m"
bs = "\033[0m"


def plugin_ss(
        command_prefix,
        command_arg_int,
        command_arg,
        # // __________________________________________
        plugin,
        name_space,
        ss_api
):
    try:
        with open(f"{script_dir}/.simple_shell_settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)

        plugin_settings = settings.get("plugin", {}).get(plugin, {})


        if plugin_settings.get("cache", False) == True and plugin in sys.modules:
            module = sys.modules[plugin]
        else:
            sys.modules.pop(plugin, None)

            file_name = plugin_settings.get('file', 'None')
            spec = importlib.util.spec_from_file_location(
                plugin,
                f"{script_dir}/plugins_ss/{file_name}.py"
            )


            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin] = module
            spec.loader.exec_module(module)


        module.command_prefix = command_prefix
        module.command_arg_int = command_arg_int
        module.command_arg = command_arg

        if plugin_settings.get("ss_api", False) == True:
            module.ss_api = ss_api

        if plugin_settings.get("load_mode", "locals") == "globals":
            module.__dict__.update(name_space)
            module.main_globals = name_space
        else:
            module.main_globals = {}

        name_space[plugin] = module

        result_plug_load = module.main()

        if plugin_settings.get("load_mode", "locals") == "globals":
            for key, value in list(module.__dict__.items()):
                name_space[key] = value

        return result_plug_load


    except Exception as e:
        post(e, 17.0)


def plugins_list():
    def check_dispatch(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                tree = ast.parse(file.read())

            for i in ast.walk(tree):
                if isinstance(i, ast.FunctionDef) and i.name == "main":
                    return True
        except Exception as e:
            post(e, 18.2)
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

        PFT(tabulate(table_data, headers=headers, tablefmt="grid"))
    except FileNotFoundError as e:
        post(e, 18.1)
    except Exception as e:
        post(e, 18.0)

