#!/usr/bin/env python

import argparse
import pathlib
import time

from pyperclip import paste

parser = argparse.ArgumentParser("Edit text files with the clipboard")
parser.add_argument("output", type=pathlib.Path)
parser.add_argument("lines", type=int, help="# lines to copy", default=1, nargs="?")
parser.add_argument(
    "--keep", "-k", type=int, default=0, help="# lines to keep in existing"
)
args = parser.parse_args()

if args.output.exists() and args.keep:
    with args.output.open() as f:
        initial = [line.strip() for line in f][: args.keep]
else:
    initial = []


def gen_clipboard():
    old_clipboard = paste()
    while True:
        time.sleep(0.2)
        new_clipboard = paste()
        if new_clipboard != old_clipboard:
            yield new_clipboard
            old_clipboard = new_clipboard


with args.output.open("w") as f:
    for line in initial:
        print(line, file=f)

    for i, line in zip(range(args.lines), gen_clipboard()):
        print(i + 1, ":", line)
        print(line, file=f)

print("Done.")
