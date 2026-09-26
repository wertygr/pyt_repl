introspection

syntax:
```text
_?_ <object> <flags>
```

**flags:**

| flag      | type      | by default |                               description                                |
|:----------|-----------|------------|:------------------------------------------------------------------------:|
| copy      | bool flag | False      |                           copy code in buffer                            |
| silent    | bool flag | False      |                          do not print on screen                          |
| dis       | mode      | Flase      |                              get byte-code                               |
| unwrap    | bool flag | False      |                           removing decorators                            |
| closure   | bool flag | Flase      |                          unwinding of closures                           |
| info      | mode      | False      |                             info for object                              |
| signature | mode      | Flase      |                              get signature                               |
| code      | mode      | True       |                             get source code                              |
| ast       | moed      | False      |                              vive ast tree                               |
| not_eval  | bool flag | Fslse      | do not attempt to retrieve the object, but rather process it as a string |
<details> <summary> example </summary>

```pycon
>>> _pyt++_
1 |def add(a: int|float, b: int|float) -> int|float:
  2 |    return a + b
>>> _?_ add
def add(a: int|float, b: int|float) -> int|float:
    return a + b

>>> _?_ add dis
  1           RESUME                   0

  2           LOAD_FAST_BORROW_LOAD_FAST_BORROW 1 (a, b)
              BINARY_OP                0 (+)
              RETURN_VALUE

>>> _?_ add ast
Module(
    body=[
        FunctionDef(
            name='add',
            args=arguments(
                args=[
                    arg(
                        arg='a',
                        annotation=BinOp(
                            left=Name(id='int', ctx=Load()),
                            op=BitOr(),
                            right=Name(id='float', ctx=Load()))),
                    arg(
                        arg='b',
                        annotation=BinOp(
                            left=Name(id='int', ctx=Load()),
                            op=BitOr(),
                            right=Name(id='float', ctx=Load())))]),
            body=[
                Return(
                    value=BinOp(
                        left=Name(id='a', ctx=Load()),
                        op=Add(),
                        right=Name(id='b', ctx=Load())))],
            returns=BinOp(
                left=Name(id='int', ctx=Load()),
                op=BitOr(),
                right=Name(id='float', ctx=Load())))])

>>> _?_ add signature
(a: int | float, b: int | float) -> int | float

>>> _?_ add info
name: add
dir: ['__annotate__', '__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__getstate__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__type_params__']
type: <class 'function'>
address: 0x7f50d81af8a0
repr: <function add at 0x7f50d81af8a0>
annotations: {'a': int | float, 'b': int | float, 'return': int | float}

>>> _?_ add info dis
  1           RESUME                   0

  2           LOAD_FAST_BORROW_LOAD_FAST_BORROW 1 (a, b)
              BINARY_OP                0 (+)
              RETURN_VALUE

>>> _?_ len_
[source_code]: no object len_

>>> _?_ len
[source_code]: The object: len cannot be get code

>>> _?_ len dis
[source_code]: The object: len cannot be disassembled

>>> _?_ len ast
[source_code]: The object: len cannot be get code

>>>
```
</details>