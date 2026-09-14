NOP = lambda *_, **__: None

SETTINGS_FILE = ".pyre_settings.json"
FILE_HISTORY = ".py_history"

PYT_SAVE = "pyt_save"
PYT_CACHE = ".pyt_save"

DEFAULT_SETTINGS = {
    "color": {},
    "plugin": {},
    "alias_dict": {},
    "posix": False,
    "shlex": False,
    "shell": False,
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