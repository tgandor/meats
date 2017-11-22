#!/usr/bin/env python

import argparse
import glob
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', '-n', action='store_true', help='Only print operations, never copy or rename')
parser.add_argument('--copy', '-c', action='store_true', help='Create copies instead of renaming')
parser.add_argument('files', nargs='+', help='')
parser.add_argument('--start', '-f', type=int, default=1, help='Starting number')
parser.add_argument('--step', '-s', type=int, default=1, help='Increment')
parser.add_argument('--pad', '-p', type=int, default=1, help='Minimal number length with leading zeros')

args = parser.parse_args()


try:
    from natsort import natsorted as sorted_function
except ImportError:
    sorted_function = sorted

move_function = (lambda x, y: None) if args.dry_run else (shutil.copy if args.copy else os.rename)

files = [f for path in args.files for f in sorted_function(glob.glob(path))]
min_padding = len(str(args.start + args.step * (len(files) - 1)))
padding = max(min_padding, args.pad)


def pad(num):
    s = str(num)
    if len(s) < padding:
        s = '0' * (padding - len(s)) + s
    return s


idx = args.start
for f in files:
    _, ext = os.path.splitext(f)
    target = pad(idx) + ext
    if os.path.exists(target):
        print('Not renamed', f, 'file exists:', target)
        continue
    print(f, '->', target)
    move_function(f, target)
    idx += args.step
