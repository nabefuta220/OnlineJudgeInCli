import submittgetter
import tracker


import argparse


def input():
    arg = argparse.ArgumentParser("sub & track")
    arg.add_argument("config")
    parse = arg.parse_args()
    return {"config": parse.config, "url": submittgetter.get_submittion_URL(submittgetter.get_data())}

if __name__ == "__main__":
    res = input()
    print(tracker.track(res['url'], res['config'], "tmp.html"))
    pass
