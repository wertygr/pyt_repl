default settings:
 ```python
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
```

You can override the default settings in the `pyre_const.py` file by modifying the `DEFAULT_SETTINGS` variable. Important: To prevent `KeyError` exceptions, ensure that all configuration keys are defined in the default settings.