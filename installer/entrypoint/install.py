import os
import stat
import string
import sys

# find writable path
path = os.getenv("PATH").split(os.pathsep)
good = []

for dirpath in path:
    writable = os.access(dirpath, os.W_OK)
    print(dirpath, ":", writable)
    if writable:
        good.append(dirpath)

if not good:
    exit("No directories writable.")

if len(good) > 1:
    print("Choose path destination:")
    paths = dict(zip(string.ascii_lowercase, good))
    for c, target in paths.items():
        print(c, "-", target)
    ans = input("Choice (default: a):").lower()
    target = paths.get(ans, paths["a"])
else:
    target = good[0]

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
            sys.executable,
            os.path.abspath(os.path.join(os.path.dirname(__file__), "execute.py")),
            "%*",
            file=mts,
        )
    print(f"Local entry point: '{LOCAL}.bat'")
