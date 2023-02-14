#!/usr/bin/env python

from os.path import dirname, exists, expanduser
import json
import os
import subprocess
import sys


if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} command/alias arguments")
    exit()

cache_path = expanduser("~/.mts_cache")

if not exists(cache_path):
    cache = {}
else:
    with open(cache_path) as cf:
        cache = json.load(cf)

alias = sys.argv[1]

if alias not in cache:
    GIT = os.path.sep + ".git"
    top = dirname(dirname(dirname(__file__)))
    found = []
    for path, dirs, files in os.walk(top):
        if GIT in path:
            continue
        for fn in files:
            if alias in fn:
                found.append(os.path.join(path, fn))
    if len(found) > 1:
        print(f"Alias {alias} is not unique. Matching files:")
        for fn in found:
            print(fn)
        exit()

    if len(found) == 0:
        print(f"Alias {alias} matched no files.")
        exit()

    entry = found[0]
    cache[alias] = entry

    with open(cache_path, "w") as cf:
        json.dump(cache, cf, indent=2)
        print(file=cf)
else:
    entry = cache[alias]

assert entry.endswith(".py")  # for now.


subprocess.call([sys.executable, entry] + sys.argv[2:])
