python repl

**install:**
```bash
mkdir pyrepl
git clone #this url
cd pyrepl
pip install req.txt
python pyre.py
```

**fast start:**
```pycon
>>> _pyt-exec_ var = "test var"
>>> _pyt-eval_ var
test var

>>> _pyt-exec_ def test_function(): pass
>>> _?_ test_function
def test_function(): pass

>>> _?_ test_function -copy -silent
>>> _pyt++_ paste
1 |def test_function():
  2 |     pass # this is multiline editor
  3 |
  4 |# Esp + Enter = exit and execute code
  5 |# Ctrl + c = exit
>>> _?_ test_function
def test_function():
     pass # this is multiline editor

>>> _pyt-exec_ g = 55 _&_ _pyt-eval_ g _&_ _?_ g
55

g = 55

>>> _#_ comment
>>> _sh_ ls /
bin  boot  dev	etc  home  lib	lib64  lost+found  mnt	opt  proc  root  run  sbin  srv  swapfile  sys	tmp  usr  var
>>> _pyt_ print(
--------------- 
eval: '(' was never closed (<py_repl_5>, line 1) 
---------------
exec: '(' was never closed (<py_repl_5>, line 1) 
---------------

>>> _pyt_ import time
>>> _pyt_ (2+88)**5
5904900000

>>> _pyt_ print(
__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ 
eval: '(' was never closed (<py_repl_7>, line 1) 
__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ 
exec: '(' was never closed (<py_repl_7>, line 1) 
__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ 

>>> _._ exit

```

| prefix                         |          arg           |                    info |
|:-------------------------------|:----------------------:|------------------------:|
| \_?_                           |   \<object> \<flag>    |           introspection |
| \_pyt++_                       |        \<flag>         |        multiline editor |
| \_pyt-exec_                    |        \<code>         |            execute code |
| \_pyt-eval_                    |        \<code>         |               eval code |
| \_._                           | \<command> \<argument> |            repl command |
| \_#_                           |       \<comment>       |                 comment |
| \<command_1> \_&_ \<command_2> |                        |                pipeline |
| \_sh_                          |       \<command>       | command on system shell |
| \_pyt_                         |        \<code>         |      auto(eval or exec) |

**req:**\
python3.12+(test on 3.14.6)\
python-jedi\
python-prompt-toolkit\
python-pygments\
python-tabulate