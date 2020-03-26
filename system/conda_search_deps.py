#!/usr/bin/env python

'''
This script is for searching reverse dependencies, i.e. "what are the users of this":
https://stackoverflow.com/questions/26101972/how-to-identify-conda-package-dependents

https://stackoverflow.com/a/52942405/1338797 says:
> conda search --reverse-dependency <package>
> should be the answer. Except it's not working.
And points to:
> https://github.com/conda/conda/issues/6670

For normal (forward) dependencies see:
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html#listing-package-dependencies
> conda info package_name
Except that:
WARNING: 'conda info package_name' is deprecated. Use 'conda search package_name --info'.

For reverse dependencies they advise:
grep numpy ~/anaconda3/pkgs/*/info/index.json

Which is cool, provided:
* you have grep (Windows?),
* you have bash (dir globbing, Windows?),
* the dependants are installed, and not just available in the channels.

BTW, .q files from .../pkgs/cache/ are just pickles:
https://github.com/conda/conda/blob/master/conda/core/subdir_data.py

'''
from __future__ import print_function

import argparse
import glob
import os

from collections import defaultdict

# this is placebo. OK, ujson looks 10% faster:
try:
    import ujson as json
except ImportError:
    import json

parser = argparse.ArgumentParser()
parser.add_argument('--save-channels', help='filename for saving all channels (JSON)')
parser.add_argument('--save', '-s', help='filename for saving reverse dependencies (JSON)')
parser.add_argument('packages', nargs='*', help='packages to check reverse deps')
args = parser.parse_args()

info = json.load(os.popen('conda info --json'))

print('Loading channels...')
channels = [
    json.load(open(repodata))
    for pkg_dir in info['pkgs_dirs']
    for repodata in glob.glob(os.path.join(pkg_dir, 'cache', '*.json'))
]
# print('Done')

if args.save_channels:
    print('Saving channels to:', args.save_channels)
    with open(args.save_channels, 'w') as all_data:
        json.dump(channels, all_data, indent=2)

rdeps = defaultdict(set)

for c in channels:
    for k, v in c['packages'].items():
        package = '-'.join(k.split('-')[:-2])
        for dep in v['depends']:
            dependant = dep.split()[0]
            rdeps[dependant].add((package, c['_url']))

if args.save:
    print('Saving rdeps to:', args.save)
    with open(args.save, 'w') as all_data:
        # not playing around with JSONEncoder for handling sets
        json.dump({k: sorted(vv[0] for vv in v) for k, v in rdeps.items()}, all_data, indent=2)

for package in args.packages:
    print(package, 'dependants:')
    for p, url in sorted(rdeps[package]):
        print(p, url, sep='\t')
    print()
