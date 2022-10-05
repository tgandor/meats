#!/usr/bin/env python

import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")
args = parser.parse_args()

os.makedirs("mirror", exist_ok=True)

i = 1
for path in args.files:
    shutil.copy(path, os.path.join("mirror", f"{i:05d}_{os.path.basename(path)}"))
    i += 1
for path in reversed(args.files):
    shutil.copy(path, os.path.join("mirror", f"{i:05d}_{os.path.basename(path)}"))
    i += 1
