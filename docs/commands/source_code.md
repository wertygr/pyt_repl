introspection

```pycon
_?_ <object> <flags>
```

**flag:**

| flag    |      description       |
|:--------|:----------------------:|
| copy    |  copy code in buffer   |
| silent  | do not print on screen |
| dis     |    disasembly code     |
| unwrap  |                        |
| closure |                        |

```pycon
>>> _?_ len
Return the number of items in a container.

>>> _?_ len_
[source_code]: no object len_

>>> _?_ len dis
[source_code]: The object: len cannot be disassembled

>>>
```