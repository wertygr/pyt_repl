commands table

| name            | require args |                               description |
|:----------------|--------------|------------------------------------------:|
| clear           | 2            |                             clear console |
| exit            | 2            |                                      exit |
| settings_reload | 2-3          |                 reread settings from disk |
| run             | 3            |                                run script |
| read_vf         | 3            |                       read linecache file |
| unload_plugin   | 3            |             unloading plugins from memory |
| ls_vf           | 2            |                                   list vf |
| del_vf          | 3            |                    delete line cache file |
| critical_error  | 2            | artificial triggering of a critical error |
| hook_run        | 4            |                      artificial hook call |
| load_plugin     | 3            |                    artificial plugin call |