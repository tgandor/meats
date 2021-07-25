#!/usr/bin/env python

import argparse
import codecs
import re
import requests

PATTERN = codecs.encode("uggcf://jjj.vafgntenz.pbz/c/([^/]+)/", "rot_13")

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("--list", "-l", action="store_true")
args = parser.parse_args()

data = requests.get(args.url).text

if not args.list:
    import instalooter.cli

    tokens = set(re.findall(PATTERN, data))
    il_args = ["-T", "{username}-{datetime}-{code}", "post"]
    for token in tokens:
        instalooter.cli.main(il_args + [token])
else:

    print("\n".join(x for x, _ in sorted(set(re.findall(f"({PATTERN})", data)))))
