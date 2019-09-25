#!/usr/bin/env python

import os
import sys


def main():
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
        target_dir = os.getcwd()
    else:
        source_dir = target_dir = os.getcwd()

    os.chdir(source_dir)
    last_commit = os.popen("git log -1").readlines()
    author_line = [line for line in last_commit if line.startswith('Aut')][0]
    author = author_line.split()

    os.chdir(target_dir)
    cmd = 'git config user.name "{}"'.format(' '.join(author[1:-1]))
    print(cmd)
    os.system(cmd)
    cmd = 'git config user.email "{}"'.format(author[-1][1:-1])
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
