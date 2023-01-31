#!/usr/bin/env python

import argparse
import contextlib
import itertools
import pathlib
import time
import sys

from pyperclip import paste


def gen_clipboard(first=False):
    old_clipboard = paste()
    if first:
        yield old_clipboard
    while True:
        time.sleep(0.2)
        new_clipboard = paste()
        if new_clipboard != old_clipboard:
            yield new_clipboard
            old_clipboard = new_clipboard


def save(line, path, mode):
    print(line)
    if path is not None:
        with open(path, mode) as f:
            print(line, file=f)


def main():
    parser = argparse.ArgumentParser("Save text files from the clipboard")
    parser.add_argument("output", type=pathlib.Path, nargs="?")
    parser.add_argument(
        "--all", "-a", action="store_true", help="save the initial clipboard contents"
    )
    parser.add_argument("--mode", "-m", help="file mode (a/w)", default="a")
    args = parser.parse_args()

    for line in gen_clipboard(args.all):
        save(line, args.output, args.mode)

if __name__ == "__main__":
    main()
