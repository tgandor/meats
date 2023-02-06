#!/usr/bin/env python

import argparse
import subprocess
import time

from pyperclip import paste

MARKER = "{}"

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument("--single-word", "-S", action="store_true")
parser.add_argument("args", nargs=argparse.REMAINDER)
opts = parser.parse_args()

args = opts.args

if not any(MARKER in arg for arg in args):
    args.append(MARKER)

old = paste()

while True:
    time.sleep(0.1)
    new = paste()
    if new != old:
        old = new

        if opts.single_word and len(new.split()) > 1:
            print("Skipping:", new)
            continue

        command = [arg.replace(MARKER, new) for arg in args]
        if opts.verbose:
            print(command)
        try:
            subprocess.call(command)
        except FileNotFoundError as e:
            print("Warning, run failed:", e)
