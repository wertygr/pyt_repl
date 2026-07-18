command_prefix = None
command_arg_int = None
command_arg = []
ss_api = {}

def dispatch_plugin():
    code_to_run = command_prefix

    if not code_to_run and command_arg:

        actual_args = command_arg[1:] if len(command_arg) > 1 else command_arg
        code_to_run = " ".join(actual_args)

    if not code_to_run:
        return

    from lua_daemon import get_daemon
    daemon = get_daemon(ss_api["script_dir"])

    if code_to_run == "__EXIT__":
        daemon.shutdown()
        return

    try:
        result = daemon.eval(code_to_run)
        if result is not None and result != "":
            print(result, flush=True)
    except RuntimeError:
        try:
            daemon.exec(code_to_run)
        except RuntimeError as e:
            print(f"Lua Syntax Error: {e}", flush=True)

