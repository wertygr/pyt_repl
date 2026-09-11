import inspect
import dis
import types
from typing import Callable, Any, Type

class DisassemblyError(Exception):
    pass
class GetObjectError(Exception):
    pass

def mode_info(obj, *_) -> str:
    info: tuple[str|None, ...] = (
        None if not hasattr(obj, "__name__") else f"name: {obj.__name__}",
        f"dir: {dir(obj)}",
        f"type: {type(obj)}",
        f"address: {hex(id(obj))}",
        None if not hasattr(obj, "__annotations__") else f"annotations: {getattr(obj, '__annotations__')}",
        getattr(obj, "__doc__", None),
        None if not hasattr(obj, "__file__") else f"file: {obj.__file__}",
    )
    return "\n".join(i for i in info if i)

def mode_normal(obj, *_) -> str:
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

def mode_dis(obj, obj_name) -> str|DisassemblyError:
    try:
        return dis.Bytecode(obj).dis()
    except TypeError:
        return DisassemblyError(f"The object: {obj_name} cannot be disassembled")

def get_source_code(
        obj_name:    str|Callable[..., Any]|Type[Any]|Any,
        namespace:   dict,
        mode:        str,
        use_unwrap:  bool,
        use_closure: bool
    ) -> str|DisassemblyError|GetObjectError:
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
    return {
        "normal": mode_normal,
        "dis":    mode_dis,
        "info":   mode_info,
    }[mode](obj, obj_name)