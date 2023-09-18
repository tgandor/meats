#!/usr/bin/env python

import webbrowser
import argparse
import pathlib
import re
import time

from pyperclip import paste


def gen_clipboard():
    old_clipboard = paste()
    while True:
        try:
            time.sleep(0.2)
        except KeyboardInterrupt:
            break
        new_clipboard = paste()
        if new_clipboard != old_clipboard:
            yield new_clipboard
            old_clipboard = new_clipboard


def main():
    parser = argparse.ArgumentParser("Dispatch copied URLs to webbrowser.")
    parser.add_argument("pattern_file", type=pathlib.Path, nargs="?")
    args = parser.parse_args()

    if args.pattern_file is None:
        patterns = [("https?://[^ ]+", "{match}")]
    else:
        with open(args.pattern_file) as pf:
            patterns = [line.strip().split(" ", 2) for line in pf]

    for line in gen_clipboard():
        for pat, target in patterns:
            if m := re.fullmatch(pat, line):
                url = target.format(match=m.group())
                print("Opening:", url)
                webbrowser.open(url)


if __name__ == "__main__":
    main()
