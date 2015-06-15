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
    some_data = open(f).read(2**12)
    date_match = re.search('\d{4}([ :]\d\d){5}', some_data)
    if not date_match:
        print 'No date information in:', f
        return
    new_name = date_match.group().replace(' ', '_').replace(':', '-') + '.jpg'
    if not os.path.exists(new_name):
        print f, '->', new_name
        os.rename(f, new_name)
    else:
        print f, '-!>', new_name, '(file exists)'

if __name__=='__main__':
    args, opts = classify(sys.argv[1:], lambda x: x.startswith('-'))
    # print (opts, args)
    map(rename, sys.argv[1:])
