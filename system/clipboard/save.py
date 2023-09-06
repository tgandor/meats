#!/usr/bin/env python

import argparse
import pathlib
import re
import time

from pyperclip import paste


def gen_clipboard(first=False):
    old_clipboard = paste()
    if first:
        yield old_clipboard
    while True:
        try:
            time.sleep(0.2)
        except KeyboardInterrupt:
            break
        new_clipboard = paste()
        if new_clipboard != old_clipboard:
            yield new_clipboard
            old_clipboard = new_clipboard


def save(line, path, mode):
    print(line)
    if path is not None:
        with open(path, mode) as f:
            print(line, file=f)


def date_to_iso(line, time=False):
    from dateutil.parser import parse, ParserError

    if not re.match(r"[0-9 :/AMPT+-]+$", line):
        return line

    try:
        date = parse(line)
    except ParserError:
        return line

    if time:
        return date.strftime("%Y-%m-%d %H:%M")
    return date.strftime("%Y-%m-%d")


def _transform(line, args):
    if args.parse_timestamps:
        return date_to_iso(line, True)
    if args.parse_dates:
        return date_to_iso(line)
    return line


def main():
    parser = argparse.ArgumentParser("Save text files from the clipboard")
    parser.add_argument("output", type=pathlib.Path, nargs="?")
    parser.add_argument(
        "--all", "-a", action="store_true", help="save the initial clipboard contents"
    )
    parser.add_argument(
        "--mode", "-m", help="file mode (a/w)", default="a", choices=["a", "w"]
    )
    parser.add_argument("--parse-dates", action="store_true")
    parser.add_argument("--parse-timestamps", action="store_true")
    args = parser.parse_args()

    for line in gen_clipboard(args.all):
        line = _transform(line, args)
        save(line, args.output, args.mode)


if __name__ == "__main__":
    main()
