#!/usr/bin/env python

import argparse
import re
import sys


def polish_monocharacters(text):
    phase1 = re.sub(r"\b([iwzoua]) (\w|\(|\\)", r"\1~\2", text, flags=re.IGNORECASE)
    phase2 = re.sub(r"~([iwzoua]) (\w|\(|\\)", r"~\1~\2", phase1)
    return phase2


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("--inplace", "-w", action="store_true")
    args = parser.parse_args()

    if not args.files:
        data = sys.stdin.read()
        result = polish_monocharacters(data)
        sys.stdout.write(result)

    for filename in args.files:
        with open(filename) as f:
            data = f.read()

        result = polish_monocharacters(data)

        if args.inplace:
            with open(filename, "w") as f:
                f.write(result)
        else:
            sys.stdout.write(result)


if __name__ == "__main__":
    _main()
