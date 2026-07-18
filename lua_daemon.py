import subprocess
import atexit

class LuaDaemon:
    def __init__(self, script_path):
        self.process = subprocess.Popen(
            ["lua", script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        ready_line = self.process.stderr.readline()
        if ready_line.strip() != "LUA_DAEMON_READY":
            raise RuntimeError("Lua daemon не стартанул")
        atexit.register(self.shutdown)

    def _send_code(self, mode, code):
        # Железная защита от None
        if code is None:
            code = ""
        clean_code = str(code).replace("\n", " ").strip()

        self.process.stdin.write(f"{mode}\n")
        self.process.stdin.write(f"{clean_code}\n")
        self.process.stdin.flush()

        while True:
            response = self.process.stdout.readline().strip()

            # Выводим логи из Lua мгновенно благодаря flush=True
            if response.startswith("__LOG__ "):
                print(response[8:], flush=True)
                continue

            if response.startswith("__ERR__ "):
                raise RuntimeError(response[8:])

            return response

    def eval(self, code):
        response = self._send_code("__EVAL__", code)
        if response.startswith("__OK__ "):
            return response[7:]
        return None

    def exec(self, code):
        return self._send_code("__EXEC__", code)

    def shutdown(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write("__EXIT__\n")
                self.process.stdin.flush()
                self.process.wait(timeout=1)
            except:
                self.process.kill()

_daemon = None

def get_daemon(script_dir):
    global _daemon
    if _daemon is None:
        _daemon = LuaDaemon(f"{script_dir}/plugins_ss/main.lua")
    return _daemon
