#!/usr/bin/env python

"""
Print branches which are merged or have children.
Can generate script to remove them from the working copy and remote.
"""
from __future__ import print_function

import argparse
import glob
import itertools
import os
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--script', '-s', action='store_true', help='Output commands for deleting remote branches')
    parser.add_argument('--limit', '-n', type=int, help='Max branches to delete')
    parser.add_argument('--include', '-i', help='only consider branches matching regular expression')
    parser.add_argument('--exclude', '-x', help='ignore branches matching regular expression')

    args = parser.parse_args()

    root_directory = os.path.abspath(os.sep)
    git_directory = None

    for i in itertools.count():
        parent_dir = os.path.join('.', *(['..'] * i))
        git_directory = os.path.join(parent_dir, '.git')
        if os.path.isdir(git_directory):
            break
        if os.path.abspath(parent_dir) == root_directory:
            raise OSError('.git directory not found here or above')

    branches = dict(
        (open(f).read().strip(), '/'.join(f.replace(git_directory, '').split(os.sep)[3:]))
        for f in itertools.chain(
            glob.glob(os.path.join(git_directory, 'refs', 'heads', '*')),
            glob.glob(os.path.join(git_directory, 'refs', 'remotes', '*', '*'))
        )
        if os.path.isfile(f)
    )

    parents = set()
    for line in os.popen('git rev-list --all --parents'):
        for commit in line.split()[1:]:
            parents.add(commit)

    candidates = [name for commit, name in branches.items() if commit in parents]

    if args.include:
        candidates = list(filter(re.compile(args.include).search, candidates))

    if args.exclude:
        excluded = list(filter(re.compile(args.exclude).search, candidates))
        if not args.script:
            for name in excluded:
                print('Skipping {} (matches "{}")'.format(name, args.exclude))
        candidates = list(set(candidates) - set(excluded))
        print()

    if not args.script:
        if not candidates:
            print('No merged branches found.')
            exit()

        print('Potentially deletable branches:\n'
              '(remember to have everything pushed & pulled)\n'
              '(also recommended: git fetch -p)\n')
        for c in candidates:
            print(c)
        print()
        print('Execute with -s to generate script to remove them.')
    else:
        for i, name in enumerate(candidates):
            if args.limit and i == args.limit:
                break

            if '/' in name:
                print('git push {} --delete {}'.format(*name.split('/', 1)))
                # this seems to never be required lately.
                # print('git branch -dr {}'.format(name))
            else:
                print('git branch -d {}'.format(name))
