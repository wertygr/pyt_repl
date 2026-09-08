RESET = "\033[0m"
YELLOW = "\033[33m"

NO_OP = lambda *_, **__: None

SETTINGS_FILE = ".pyre_settings.json"
FILE_HISTORY = ".py_history"

DEFAULT_SETTINGS = {
    "color": {},
    "plugin": {},
    "alias_dict": {},
    "posix": False,
    "shlex": False,
    "vi_mode": False,
    "multiline": False,
    "separator": False,
    "alias_locals": False,
    "mouse_support": False,
    "alias_globals": False,
    "bottom_toolbar": False,
    "shell_container": False,
    "prompt": ">>> ",
    "repl_mode": "locals",
    "line_name_format": "{line_number} |"
}