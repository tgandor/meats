#!/usr/bin/env python

import argparse
import glob
import itertools
import os
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('file_patterns', nargs='+')
parser.add_argument('--dry-run', '-n', action='store_true')
parser.add_argument('--ignore-suffix', action='store_true')
args = parser.parse_args()

# this is because of a gotcha, when expanded (or not) file patterns
# contain something like '[text]' - then the glob will expect no [] and 1 character there...
patterns = [p for p in args.file_patterns if not os.path.exists(p)]
files = [f for f in args.file_patterns if os.path.exists(f)]
# look how many ways there are to do it...
files = sum(map(glob.glob, patterns), files)


def pad(num, max_len):
    zeros = max(0, max_len - len(num))
    return '0'*zeros + num


GROUP_REGEX = r'\d+.*' if args.ignore_suffix else r'\d+'

for _, group in itertools.groupby(files, lambda x: re.sub(GROUP_REGEX, '', x)):
    members = list(group)
    if len(members) == 1:
        print('Single file: {0}'.format(members[0]))
        continue
    pairs = [(x, re.search(r'\d+', x).group()) for x in members]
    max_len = max(len(p[1]) for p in pairs)
    renames = [
        (name, re.sub(r'\d+', pad(num, max_len), name))
           for name, num in pairs
           if len(num) < max_len
       ]

    for old_name, new_name in renames:
        if not os.path.exists(new_name):
            if not args.dry_run:
                os.rename(old_name, new_name)
            print('{0} -> {1}'.format(old_name, new_name))
        else:
            print('Names conflict: {0} - not saved!'.format(new_name))
