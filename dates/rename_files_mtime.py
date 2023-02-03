#!/usr/bin/env python

import argparse
import datetime
import glob
import itertools
import os

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")
parser.add_argument("--format", "-f", default="%Y%m%d_%H%M%S")
parser.add_argument("--dry-run", "-n", action="store_true")
args = parser.parse_args()

files = sorted(itertools.chain.from_iterable(map(glob.glob, args.files)))

for fn in files:
    base, ext = os.path.splitext(fn)
    stat = os.stat(fn)
    name = datetime.datetime.fromtimestamp(stat.st_mtime).strftime(args.format) + ext

    if name == fn:
        print(fn, "already correct")
        continue

    print(fn, '->', name)

    if os.path.exists(name):
        print("Error:", name, "exists")
        continue

    if args.dry_run:
        continue

    os.rename(fn, name)
