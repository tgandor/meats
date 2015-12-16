#!/usr/bin/env python

import glob
import itertools
import os
import re
import sys

files = sum(map(glob.glob, sys.argv[1:]), [])

def pad(num, max_len):
    zeros = max(0, max_len - len(num))
    return '0'*zeros + num

for _, group in itertools.groupby(files, lambda x: re.sub(r'\d+', '', x)):
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
            os.rename(old_name, new_name)
            print('{0} -> {1}'.format(old_name, new_name))
        else:
            print('Names conflict: {0} - not saved!'.format(new_name))

