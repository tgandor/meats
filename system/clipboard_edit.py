#!/usr/bin/env python

import argparse
import contextlib
import itertools
import pathlib
import time
import sys

from pyperclip import paste


@contextlib.contextmanager
def open_out(output):
    if output is None:
        yield sys.stdout
    else:
        with output.open("w") as f:
            yield f


def gen_clipboard():
    old_clipboard = paste()
    while True:
        time.sleep(0.2)
        new_clipboard = paste()
        if new_clipboard != old_clipboard:
            yield new_clipboard
            old_clipboard = new_clipboard


def main():
    parser = argparse.ArgumentParser("Edit text files with the clipboard")
    parser.add_argument("output", type=pathlib.Path, nargs="?")
    parser.add_argument("lines", type=int, help="# lines to copy", default=1, nargs="?")
    parser.add_argument(
        "--keep", "-k", type=int, default=0, help="# lines to keep in existing"
    )
    args = parser.parse_args()
    verbose = True
    igen = range(args.lines)

    if args.output is None:
        # special case: print new CB to stdout
        verbose = False
        initial = []
        igen = itertools.count()
    elif args.output.exists() and args.keep:
        with args.output.open() as f:
            initial = [line.strip() for line in f][: args.keep]
    else:
        initial = []

    with open_out(args.output) as f:
        for line in initial:
            print(line, file=f)

        for i, line in zip(igen, gen_clipboard()):
            if verbose:
                print(i + 1, ":", line)
            print(line, file=f, flush=True)
    if verbose:
        print("Done.")


if __name__ == "__main__":
    main()
