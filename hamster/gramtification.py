#!/usr/bin/env python

import argparse
import re
import requests
import sys

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('--list', action='store_true')
args = parser.parse_args()

data = requests.get(args.url).text

if not args.list:
    import instalooter.cli
    tokens = set(re.findall('https://www.instagram.com/p/([^/]+)/', data))
    il_args = ["-T", "{username}-{datetime}-{code}", "post"]
    for token in tokens:
        instalooter.cli.main(il_args + [token])
else:
    print('\n'.join(sorted(set(re.findall('https://www.instagram.com/p/[^/]+/', data)))))
