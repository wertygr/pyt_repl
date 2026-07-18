
command_prefix = None
command_arg_int = None
command_arg = []

ss_api = {}

command = command_arg[0:]


def dispatch_plugin():

    err = ss_api["err"]
    bs = ss_api["bs"]
    YELLOW = ss_api["YELLOW"]
    settings = ss_api["settings"]
    simple_shell = ss_api["simple_shell"]
    script_dir = ss_api["script_dir"]
    script_file = ss_api["script_file"]
    pyt_lex = ss_api["pyt_lex"]
    post = ss_api["post"]
    PFT = ss_api["PFT"]
    
    print(command_arg)
    command_separators = ss_api["command_separators"]

    print(err)
    post()
    print(bs)
    PFT("плагин тест PFT, pyt_lex")

    print(command_arg)

    print(command_separators(command_arg))