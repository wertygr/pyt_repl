command_prefix = None
command_arg_int = None
command_arg = []
ss_api = {}
def main():
    import time

    PFT = ss_api["PFT"]
    pars = ss_api["pars_command"]
    pt_style = ss_api["pt_style"]
    start_time = time.perf_counter()
    pars(command_prefix)
    end_time = time.perf_counter()
    PFT((end_time - start_time), pt_style)