#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', '-n', action='store_true')
parser.add_argument('files', nargs='+')
args = parser.parse_args()


def maybe_rename(filename, old, new):
    if old != new:
        new_name = filename.replace(old, new)

        if new_name == filename:
            return filename

        if not os.path.exists(new_name):
            print(filename, ' ->', new_name, '(dry run)' if args.dry_run else '')
            if not args.dry_run:
                os.rename(filename, new_name)
            return new_name
        else:
            print(filename)
            print('  Cannot rename, already exists:', new_name)

    return filename


def gen_files(args):
    for pattern in args.files:
        if os.path.exists(pattern):
            yield pattern
        else:
            for filename in glob.glob(pattern):
                yield filename


def main():
    for filename in gen_files(args):
        date = re.search(r'((?:19|20)\d\d)[-_](\d+)[-_](\d+)', filename)
        if date:
            old_date = date.group()
            new_date = '-'.join('%02d' % int(g) for g in date.groups())
            filename = maybe_rename(filename, old_date, new_date)


        time = re.search(r'(\d+)h(\d+)m(\d+)s', filename)
        if time:
            old_time = time.group()
            new_time = '%02dh%02dm%02ds' % tuple(map(int, time.groups()))
            filename = maybe_rename(filename, old_time, new_time)

if __name__ == '__main__':
    main()
