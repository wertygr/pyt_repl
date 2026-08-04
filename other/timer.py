import time

def main(ss_api, command_context) -> dict:
    PFT      = ss_api["PFT"]
    pars     = ss_api["pars_command"]
    data     = ss_api["data"]

    data.command = data.command_prefix
    start_time = time.perf_counter()
    pars(data)
    end_time = time.perf_counter()

    PFT((end_time - start_time), ss_api["data"])
    return {}