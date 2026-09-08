from prompt_toolkit.enums import EditingMode
from prompt_toolkit.application.current import get_app
from pyre_core import Data

def bottom_toolbar(data: Data) -> str:
    app = get_app()
    if app.editing_mode == EditingMode.VI:
        vi_mode_name = str(app.vi_state.input_mode)
        mode_str = vi_mode_name.split(".")[-1]
        return mode_str
    return ""
