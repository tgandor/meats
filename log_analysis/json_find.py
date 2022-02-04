#!/usr/bin/env python

import argparse
import json
import sys


def search_recursive(data, pattern, path=None):
    if path is None:
        path = []

    if type(data) in (int, float, str):
        if pattern in str(data):
            print("[" + "][".join(repr(x) for x in path) + "]\n   ", data)
    elif type(data) is list:
        for i, val in enumerate(data):
            search_recursive(val, pattern, path + [i])
    elif type(data) is dict:
        for key, val in data.items():
            search_recursive(val, pattern, path + [key])


parser = argparse.ArgumentParser()
parser.add_argument("json_file")
parser.add_argument("pattern")
args = parser.parse_args()

stream = sys.stdin if args.json_file == "-" else open(args.json_file)
data = json.load(stream)
search_recursive(data, args.pattern)
