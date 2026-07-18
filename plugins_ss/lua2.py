import lupa

command_prefix = None
command_arg_int = None
command_arg = None
ss_api = {}

_persistent_lua_runtime = None


class PluginBridge:
    def get_global(self, name):
        # Динамически берем main_globals из глобальной области видимости плагина
        ns = globals().get('main_globals')
        if isinstance(ns, dict) and name in ns:
            return ns[name]
        return globals().get(name)

    def set_global(self, name, value):
        # Пишем в main_globals, который plugin_ss синхронизирует с ядром
        ns = globals().get('main_globals')
        if isinstance(ns, dict):
            ns[name] = value

        # Также пишем в globals самого плагина
        globals()[name] = value


def _get_shared_runtime():
    global _persistent_lua_runtime
    if _persistent_lua_runtime is None:
        lr = lupa.LuaRuntime(unpack_returned_tuples=True)
        # Просто создаем мост, теперь он сам будет искать main_globals при вызовах
        lr.globals().python = lupa.as_attrgetter(PluginBridge())
        _persistent_lua_runtime = lr
    return _persistent_lua_runtime

def dispatch_plugin():
    post = ss_api["post"]
    if not command_prefix:
        return

    lua = _get_shared_runtime()

    # Если команда похожа на вызов метода/функции, лучше использовать execute, а не eval
    if "(" in command_prefix or " " in command_prefix:
        try:
            lua.execute(command_prefix)
            return
        except lupa.LuaError as e:
            if isinstance(ss_api, dict) and 'post' in ss_api:
                full_error_msg = f"{ss_api.get('err', '')} {e}".strip()
                ss_api["post"](full_error_msg, 30)
            else:
                print(f"Lua error: {e}")
            return

    # Для простых переменных оставляем старую логику
    try:
        result = lua.eval(f"return {command_prefix}")
        print(result)



    except lupa.LuaError:
        try:
            lua.execute(command_prefix)
        except lupa.LuaError as e:
            if isinstance(ss_api, dict) and 'post' in ss_api:
                # post(e, 30)
                # # ss_api["post"](ss_api.get("err", ""), str(e), 30)
                full_error_msg = f"{ss_api.get('err', '')} {e}".strip()
                post(full_error_msg, 30)
            else:
                print(f"Lua error: {e}")
