#!/usr/bin/env python

import argparse
import os
import stat
import string
import sys
import uuid


def is_writable(dirpath):
    if sys.platform.startswith("linux"):
        return os.access(dirpath, os.W_OK)

    try:
        test_file = os.path.join(dirpath, str(uuid.uuid4()) + ".txt")
        with open(test_file, "w") as test:
            test.write("hello")
        os.unlink(test_file)
        return True
    except OSError as e:
        print(e)
        return False


def find_writable_path():
    path = os.getenv("PATH").split(os.pathsep)  # type: ignore
    good = []

    for dirpath in path:
        writable = is_writable(dirpath)
        print(dirpath, ":", writable)
        if writable:
            good.append(dirpath)

    if not good:
        exit("No directories writable.")

    if len(good) > 1:
        print("Choose path destination:")
        paths = dict(zip(string.ascii_letters, good))
        for c, target in paths.items():
            print(c, "-", target)
        ans = input("Choice (default: a): ")
        target = paths.get(ans, paths["a"])
    else:
        target = good[0]

    return target


parser = argparse.ArgumentParser()
parser.add_argument("--dest", "-d")
args = parser.parse_args()

if "VIRTUAL_ENV" not in os.environ or "pypoetry" not in os.environ["VIRTUAL_ENV"]:
    ans = input(
        f"Not running inside Poetry. Install for this Python {sys.executable}? (N/y) "
    )
    if ans.lower() != "y":
        exit("Cancelled.")

target = args.dest or find_writable_path()
print("Installing to directory:", target)

LOCAL = os.path.join(target, "mts")
if sys.platform.startswith("linux"):
    with open(LOCAL, "w") as mts:
        print("#!/bin/bash", file=mts)
        print(
            sys.executable,
            os.path.abspath(os.path.join(os.path.dirname(__file__), "execute.py")),
            '"$@"',
            file=mts,
        )
    mode = os.stat(LOCAL).st_mode
    os.chmod(LOCAL, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Local entry point: '{LOCAL}'")
else:
    with open(LOCAL + ".bat", "w") as mts:
        print("@echo off", file=mts)
        print(
            f'"{sys.executable}"',
            f'"{os.path.abspath(os.path.join(os.path.dirname(__file__), "execute.py"))}"',
            "%*",
            file=mts,
        )
    print(f"Local entry point: '{LOCAL}.bat'")
