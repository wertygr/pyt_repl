run command in shell\
example:
```pycon
>>> _sh_ ls /
bin  boot  dev	etc  home  lib	lib64  lost+found  mnt	opt  proc  root  run  sbin  srv  swapfile  sys	tmp  usr  var
>>>
```

<details> <summary> shell container </summary>

activate in [settings](../settings/settings.md)\
example:

```pycon
>>> _pyt-exec_ test_var = "test var"
>>> _sh_ echo $test_var
test var
```

syntax:
```text
_sh_  $<var>
  ^   ^  ^
  |   |  |______ variable that will be substituted
  |   |_________ substitution indication
  |_____________ prefix
```
_works on the principle of text replacement_
</details>