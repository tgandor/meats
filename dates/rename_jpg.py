#!/usr/bin/env python

# usage: rename_jpg.py dscn0001.jpg...

import os
import re
import sys


def classify(iterable, func):
    results = {False: [], True: []}
    for i in iterable:
        results[func(i)].append(i)
    return results.values()


def rename(f):
    some_data = open(f, 'rb').read(2**12)
    date_match = re.search(b'\d{4}([ :]\d\d){5}', some_data)
    if not date_match:
        print('No date information in: {}'.format(f))
        return
    new_name = date_match.group().decode().replace(' ', '_').replace(':', '-') + '.jpg'
    if not os.path.exists(new_name):
        print('{} -> {}'.format(f, new_name))
        os.rename(f, new_name)
    else:
        print('{} -!> {} (file exists)'.format(f, new_name))

if __name__=='__main__':
    args, opts = classify(sys.argv[1:], lambda x: x.startswith('-'))
    # print (opts, args)
    list(map(rename, sys.argv[1:]))
