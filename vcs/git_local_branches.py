#!/usr/bin/env python

"""
List branches, which are not in any remote.
They may be new, or someone might deleted them from the remote accidentaly.
"""

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--force", "-f", action="store_true", help="use -D for deleting")
parser.add_argument("--run", action="store_true", help="execute commands directly")
args = parser.parse_args()

branches = {
    line[2:].strip() for line in os.popen("git branch -a") if " -> " not in line
}

remotes = {
    "/".join(branch.split("/")[2:])
    for branch in branches
    if branch.startswith("remotes/")
}

local_branches = set(filter(lambda x: not x.startswith("remotes/"), branches))

commands = ["git branch -d {}".format(branch) for branch in (local_branches - remotes)]

if not args.run:
    if commands:
        print("\n".join(commands))
else:
    for cmd in commands:
        print(cmd)
        os.system(cmd)
    if not commands:
        print("Nothing to do.")
