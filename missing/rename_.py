#!/usr/bin/env python

import argparse
import glob
import os
import re
import sys
from itertools import chain


def rename(f, replace_function, dry_run=False):
    target = replace_function(f)
    if f == target:
        print ('File: {0} - not affected.'.format(f))
        return

    if not os.path.exists(target):
        print ('Moving: {0} -> {1}'.format(f, target))
        if not dry_run:
            os.rename(f, target)
    else:
        print ('Error! File exists: {0}'.format(target))


def fake_rename(f, replace_function):
    rename(f, replace_function, True)


def regex_replacer(search, replace):
    regex = re.compile(search)

    def do_replace(filename):
        return regex.sub(replace, filename)
    return do_replace


def string_replacer(search, replace):
    def do_replace(filename):
        return filename.replace(search, replace)
    return do_replace


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--regexp', '-x', help='Use regular expression for searching', action='store_true')
    parser.add_argument('--dry-run', '-n', help='Do not rename anything, just print messages', action='store_true')
    parser.add_argument('--no-glob', help='treat arguments verbatim, without trying to glob', action='store_true')
    parser.add_argument('search', help='Search string or regular expression')
    parser.add_argument('replace', help='Replacement string/expression')
    parser.add_argument('files', nargs='+', help='Files to rename')
    args = parser.parse_args()

    renamer = fake_rename if args.dry_run else rename

    if args.regexp:
        replacer = regex_replacer(args.search, args.replace)
    else:
        replacer = string_replacer(args.search, args.replace)

    files = args.files if args.no_glob else chain(*(glob.glob(g) for g in args.files))

    for fn in files:
        renamer(fn, replacer)
