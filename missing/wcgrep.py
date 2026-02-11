#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("search")
parser.add_argument("--all", "-a", action="store_true")
parser.add_argument("--list", "-l", action="store_true")
parser.add_argument("--quiet", "-q", action="store_true")
args = parser.parse_args()

search = args.search
skip_patterns = [
    "__pycache__",
    ".git",
    ".hg",
    ".mypy_cache",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "node_modules",
]

for directory, _, files in os.walk("."):
    if any(pattern in directory for pattern in skip_patterns):
        continue
    for f in files:
        if f.startswith(".") and not args.all:
            continue
        full_name = os.path.join(directory, f)
        with open(full_name) as lines:
            nl = 0
            try:
                for line in lines:
                    nl += 1
                    if search in line:
                        if args.list:
                            print(full_name)
                            break
                        print(full_name, ":", nl, ":", line.rstrip())
            except UnicodeDecodeError:
                if not args.quiet:
                    print("Error decoding:", full_name, file=sys.stderr)
            except PermissionError:
                if not args.quiet:
                    print("Error accessing:", full_name, file=sys.stderr)
