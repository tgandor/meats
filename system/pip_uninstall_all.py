#!/usr/bin/env python

import os
import sys


KEEP = {
    "pip",
    "setuptools",
    "wheel",
}

for_real = len(sys.argv) > 1 and sys.argv[1] == '-y'

packages = os.popen(sys.executable + " -m pip freeze").read().strip().split("\n")

for line in packages:
    if "==" not in line:
        print("I don't understand this line:", line)
        continue

    name, ver = line.split("==")
    if name in KEEP:
        # seems like this never happens...
        print("Keeping", name)
        continue

    if for_real:
        print("Deleting:", name)
        os.popen(sys.executable + " -m pip uninstall " + name)
    else:
        print("Would delete:", name)

if not for_real:
    print("This is a DRY RUN. Please pass -y as only argument to really do delete.")
