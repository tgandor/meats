#!/usr/bin/env python

import argparse
import subprocess
import time

from pyperclip import paste

MARKER = "{}"

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", "-v", action="store_true")
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
        command = [arg.replace(MARKER, new) for arg in args]
        if opts.verbose:
            print(command)
        subprocess.call(command)
        old = new
