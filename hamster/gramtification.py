#!/usr/bin/env python

import argparse
import codecs
import glob
import random
import re
import time
import requests

PATTERN = codecs.encode("uggcf://jjj.vafgntenz.pbz/c/([^/]+)/", "rot_13")

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("--list", "-l", action="store_true")
parser.add_argument("--sleep", "-s", type=int, default=10)
args = parser.parse_args()

data = requests.get(args.url).text

if not args.list:
    import instalooter.cli

    tokens = sorted(set(re.findall(PATTERN, data)))
    il_args = ["-T", "{username}-{datetime}-{code}", "post"]
    for token in tokens:
        if glob.glob(f"*{token}*"):
            print(f"Skipping {token}")
            continue
        res = instalooter.cli.main(il_args + [token])
        print(f"for {token=}, {res=}")
        nap = random.randint(args.sleep, args.sleep * 2)
        print(f"Sleeping, {nap=}")
        time.sleep(nap)
else:
    print("\n".join(x for x, _ in sorted(set(re.findall(f"({PATTERN})", data)))))
