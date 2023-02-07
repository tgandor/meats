#!/usr/bin/env python

import argparse
import json
import time

import pyperclip

try:
    import yaml
except ImportError:
    pass


def get_lines(data_file):
    if data_file.endswith(".json"):
        with open(data_file) as jsf:
            data = json.load(jsf)
    elif data_file.endswith(".yml") or data_file.endswith(".yaml"):
        with open(data_file) as ymlf:
            data = yaml.safe_load(ymlf)
    else:
        with open(data_file) as text:
            data = {f"Line {i}": line.strip() for i, line in enumerate(text, start=1)}

    for key, value in data.items():
        yield key, value


parser = argparse.ArgumentParser()
parser.add_argument("data_file")
parser.add_argument("--wait", "-w", type=float, default=5)
parser.add_argument("--delay", "-d", type=float, default=2.5)
parser.add_argument("--loop", "-l", action="store_true")
args = parser.parse_args()

print(
    f"Preparing clipboard, waiting {args.wait} s... (interval will be {args.delay} s)"
)
time.sleep(args.wait)

while True:
    for title, contents in get_lines(args.data_file):
        pyperclip.copy(contents)
        print(f"Copied {title}: ", "***" if title == "password" else contents)
        time.sleep(args.delay)
    if not args.loop:
        break
