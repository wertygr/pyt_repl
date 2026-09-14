import inspect
import dis
import ast
from typing import Callable, Any, Type
class PyreInspectError(Exception):
    pass
class DisassemblyError(PyreInspectError):
    pass
class GetObjectError(PyreInspectError):
    pass
class GetSignatureError(PyreInspectError):
    pass
class GetCodeError(PyreInspectError):
    pass

def mode_ast(obj, obj_name) -> str|GetObjectError:
    try:
        result = ast.dump(
            ast.parse(inspect.getsource(obj)),
            indent=4
        )
    except (OSError, TypeError):
        result = GetObjectError(f"The object: {obj_name} cannot be get code")
    return result

def mode_signature(obj, obj_name) -> str|GetSignatureError:
    try:
        return str(inspect.signature(obj))
    except (ValueError, TypeError):
        return GetSignatureError(f"The object: {obj_name} cannot be get signature")

def mode_info(obj, *_) -> str:
    info: tuple[str|None, ...] = (
        None if not hasattr(obj, "__name__") else f"name: {obj.__name__}",
        f"dir: {dir(obj)}",
        f"type: {type(obj)}",
        f"address: {hex(id(obj))}",
        f"repr: {obj!r}",
        None if not hasattr(obj, "__file__") else f"file: {obj.__file__}",
        None if not getattr(obj, "__annotations__", None) else f"annotations: {obj.__annotations__}",
        getattr(obj, "__doc__", None),
    )
    return "\n".join(i for i in info if i)

def mode_normal(obj, obj_name) -> str|GetCodeError:
    try:
        result = inspect.getsource(obj)
    except (OSError, TypeError):
        result = GetCodeError(f"The object: {obj_name} cannot be get code")
    return result

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
    ) -> str|DisassemblyError|GetObjectError|GetSignatureError|GetCodeError:
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
        "normal":    mode_normal,
        "dis":       mode_dis,
        "info":      mode_info,
        "signature": mode_signature,
        "ast":       mode_ast,
    }[mode](obj, obj_name)