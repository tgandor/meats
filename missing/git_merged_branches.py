#!/usr/bin/env python

"""
Print branches which are merged or have children.
"""
from __future__ import print_function

import glob
import os
import argparse
import itertools


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--script', '-s', action='store_true', help='Output commands for deleting remote branches')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress printing branch names (to use with -s)')
    parser.add_argument('--limit', '-n', type=int, help='Max branches to ')

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
        ))

    parents = set()
    for line in os.popen('git rev-list --all --parents'):
        for commit in line.split()[1:]:
            parents.add(commit)

    candidates = [name for commit, name in branches.items() if commit in parents]

    if not args.quiet:
        print('Potentially deletable branches:\n'
              '(remember to have everything pushed & pulled)\n'
              '(also recommended: git fetch -p)\n')
        for c in candidates:
            print(c)
        if len(candidates):
            print()

    if args.script:
        for i, name in enumerate(candidates):
            if args.limit and i == args.limit:
                break
            if '/' in name:
                print('git push {} --delete {}'.format(*name.split('/', 1)))
                print('git branch -dr {}'.format(name))
            else:
                print('git branch -d {}'.format(name))
