#!/usr/bin/env python

import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", nargs="?")
    parser.add_argument("-g", action="store_true")
    parser.add_argument("--dry-run", "-n", action="store_true")
    args = parser.parse_args()

    target_dir = os.getcwd()
    source_dir = args.source_dir or target_dir

    os.chdir(source_dir)
    last_commit = os.popen("git log -1").readlines()
    author_line = [line for line in last_commit if line.startswith('Aut')][0]
    author = author_line.split()

    g = '--global' if args.g else ''
    os.chdir(target_dir)
    cmd = 'git config {} user.name "{}"'.format(g, ' '.join(author[1:-1]))
    print(cmd)
    if not args.dry_run:
        os.system(cmd)
    cmd = 'git config {} user.email "{}"'.format(g, author[-1][1:-1])
    print(cmd)
    if not args.dry_run:
        os.system(cmd)


if __name__ == '__main__':
    main()
