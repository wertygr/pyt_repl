introspection

```pycon
_?_ <object> <flags>
```

**flag:**

| flag      |      description       |
|:----------|:----------------------:|
| copy      |  copy code in buffer   |
| silent    | do not print on screen |
| dis       |    disasembly code     |
| unwrap    |  removing decorators   |
| closure   | unwinding of closures  |
| info      |    info for object     |
| signature |     get signature      |

```pycon
>>> _?_ len
Return the number of items in a container.

>>> _?_ len_
[source_code]: no object len_

>>> _?_ len dis
[source_code]: The object: len cannot be disassembled

>>> _?_ os.system
Execute the command in a subshell.

>>> _?_ os.system dis
[source_code]: The object: os.system cannot be disassembled

>>> _?_ json.load
def load(fp, *, cls=None, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document) to a Python object.

    ``object_hook`` is an optional function that will be called with the
    result of any object literal decode (a ``dict``). The return value of
    ``object_hook`` will be used instead of the ``dict``. This feature
    can be used to implement custom decoders (e.g. JSON-RPC class hinting).

    ``object_pairs_hook`` is an optional function that will be called with
    the result of any object literal decoded with an ordered list of pairs.
    The return value of ``object_pairs_hook`` will be used instead of the
    ``dict``.  This feature can be used to implement custom decoders.  If
    ``object_hook`` is also defined, the ``object_pairs_hook`` takes
    priority.

    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``JSONDecoder`` is used.
    """
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)

>>> _?_ json.load dis
278           RESUME                   0

298           LOAD_GLOBAL              1 (loads + NULL)
              LOAD_FAST_BORROW         0 (fp)
              LOAD_ATTR                3 (read + NULL|self)
              CALL                     0
              BUILD_TUPLE              1
              LOAD_CONST               1 ('cls')

299           LOAD_FAST_BORROW         1 (cls)

298           LOAD_CONST               2 ('object_hook')

299           LOAD_FAST_BORROW         2 (object_hook)

298           LOAD_CONST               3 ('parse_float')

300           LOAD_FAST_BORROW         3 (parse_float)

298           LOAD_CONST               4 ('parse_int')

300           LOAD_FAST_BORROW         4 (parse_int)

298           LOAD_CONST               5 ('parse_constant')

301           LOAD_FAST_BORROW         5 (parse_constant)

298           LOAD_CONST               6 ('object_pairs_hook')

301           LOAD_FAST_BORROW         6 (object_pairs_hook)

298           BUILD_MAP                6

301           LOAD_FAST_BORROW         7 (kw)

298           DICT_MERGE               1
              CALL_FUNCTION_EX
              RETURN_VALUE

>>> _?_ json.load info
name: load
dir: ['__annotate__', '__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__getstate__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__type_params__']
type: <class 'function'>
address: 0x7feac648cb40
Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
a JSON document) to a Python object.

``object_hook`` is an optional function that will be called with the
result of any object literal decode (a ``dict``). The return value of
``object_hook`` will be used instead of the ``dict``. This feature
can be used to implement custom decoders (e.g. JSON-RPC class hinting).

``object_pairs_hook`` is an optional function that will be called with
the result of any object literal decoded with an ordered list of pairs.
The return value of ``object_pairs_hook`` will be used instead of the
``dict``.  This feature can be used to implement custom decoders.  If
``object_hook`` is also defined, the ``object_pairs_hook`` takes
priority.

To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
kwarg; otherwise ``JSONDecoder`` is used.

>>>

```