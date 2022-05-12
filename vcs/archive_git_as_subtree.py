#!/usr/bin/env python

import argparse
import os


def or_die(command):
    print(command)
    result = os.system(command)
    if result != 0:
        print(f"{command} failed with code: {result}")
        exit(result)


parser = argparse.ArgumentParser()
parser.add_argument("clone_url")
args = parser.parse_args()

basename = os.path.basename(args.clone_url).replace(".git", "")
print(basename)
worktree = "r_" + basename

# clone repo
if not os.path.exists(worktree):
    or_die(f"git clone {args.clone_url} {worktree}")

# add subtree
if not os.path.exists(basename):
    os.chdir(worktree)
    branch = os.popen("git branch").read().replace("*", "").strip()
    print("Branch:", branch)

    os.chdir("..")
    or_die(f"git subtree add --prefix {basename} {worktree} {branch}")
