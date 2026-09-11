import inspect
import dis
import types
from typing import Callable, Any, Type

class DisassemblyError(Exception):
    pass
class GetObjectError(Exception):
    pass

def get_source_code(
        obj_name: str|Callable[..., Any]|Type[Any]|Any,
        namespace: dict,
        use_dis: bool,
        use_unwrap: bool,
        use_closure: bool) -> str|DisassemblyError|GetObjectError:
    code = None
    obj = obj_name
    if isinstance(obj, str):
        try:
            obj = eval(obj, namespace)
        except Exception:
            return GetObjectError(f"no object {obj_name}")
    if use_unwrap:
        obj = inspect.unwrap(obj) if isinstance(obj, Callable) else obj
    if use_closure:
        while hasattr(obj, "__closure__") and obj.__closure__:
            found_inner = False
            for cell in obj.__closure__:
                try:
                    cell_contents = cell.cell_contents
                except ValueError:
                    continue
                if callable(cell_contents):
                    obj = cell_contents
                    found_inner = True
                    break
            if not found_inner:
                break
    if use_dis:
        try:
            return dis.Bytecode(obj).dis()
        except TypeError:
            return DisassemblyError(f"The object: {obj_name} cannot be disassembled")
    else:
        if isinstance(obj, (types.ModuleType, Callable, type)):
            try:
                code = inspect.getsource(obj)
            except (OSError, TypeError):
                code = getattr(obj, "__doc__")
                if not code:
                    code = repr(obj)
        else:
            code = repr(obj)
    return code