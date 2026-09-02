auto eval or exec(eval is a priority)

example:
```pycon
>>> _pyt_ d = 444
>>> _pyt_ import time
>>> _pyt_ print(d) # eval is a priority
444
None 

>>>
```
_it is recommended to use a "[\_pyt-exec\_](pyt_exec.md)/[\_pyt-eval\_](pyt_eval.md)"_