#!/usr/bin/env python

from os.path import dirname, exists, expanduser
import json
import os
import platform
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
prefix = False
search = False

if alias.startswith("/"):
    alias = alias[1:]
    prefix = True
if alias.startswith("%"):
    alias = alias[1:]
    search = True


def _match(fn):
    if prefix:
        return fn.startswith(alias)
    return alias in fn


def _open(file_path):
    if not search:
        assert entry.endswith(".py")
        subprocess.call([sys.executable, entry] + sys.argv[2:])
        return

    if platform.system() == "Darwin":
        subprocess.run(["open", file_path])
    elif platform.system() == "Windows":
        subprocess.run(["start", file_path], shell=True)
    else:
        subprocess.run(["xdg-open", file_path])


def _crawl():
    GIT = os.path.sep + ".git"
    top = dirname(dirname(dirname(__file__)))
    found = []
    for path, dirs, files in os.walk(top):
        if GIT in path:
            continue
        for fn in files:
            if _match(fn) and (fn.endswith(".py") or search):
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

    return entry


if alias in cache:
    entry = cache[alias]
else:
    entry = _crawl()

_open(entry)
