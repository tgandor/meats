#!/usr/bin/env python

from __future__ import print_function

import os
import subprocess


def du(verbose=False):
    total = 0
    for path, _, files in os.walk('.'):
        if ('.git' + os.path.sep) in path:
            continue

        for filename in files:
            size = os.stat(os.path.join(path, filename)).st_size
            if verbose:
                print(filename, size)
            total += size

    return total


def quiet_os_system(command):
    return subprocess.call(
        command.split(),
        stdout=subprocess.PIPE,  # is'n there a "subprocess.DEVNULL" flag?
        stderr=subprocess.PIPE
    )


revisions = os.popen('git log --format=oneline').read().strip().split('\n')
num_revisions = len(revisions)

# TODO: this is not depth! ... merges can cause it to be overestimated

print(
    '#',
    'commit',
    'depth',
    'bytes',
    'human',
    'message',
    sep='\t'
)

for commit_number, line in enumerate(reversed(revisions), start=1):
    # print(repr(line))
    commit_hash = line.split()[0]
    result = quiet_os_system('git checkout ' + commit_hash)
    if result != 0:
        print('Error checking out commit', commit_number)
        exit()

    # os.system('ls')
    repo_size = du()
    print(
        commit_number,
        num_revisions - commit_number + 1,
        commit_hash,
        repo_size,
        '{:,}'.format(repo_size),
        line.replace(commit_hash, '').strip()[:60],
        sep='\t'
    )

quiet_os_system('git checkout master')