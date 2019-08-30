#!/usr/bin/env python3

from __future__ import print_function

import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--copy', '-c', action='store_true', help='copy instead of moving')
parser.add_argument('files', nargs='+')
parser.add_argument('target_directory')
args = parser.parse_args()

if os.path.exists(args.target_directory) and not os.path.isdir(args.target_directory):
    print('Target is not a directory:', args.target_directory)
    exit()

real_target = os.path.realpath(args.target_directory)
real_chunks = real_target.split('/')
if real_chunks[-1] == '':
    real_chunks.pop()

for filename in args.files:
    source_chunks = os.path.realpath(filename).split('/')

    if len(real_chunks) > len(source_chunks):
        print('Too deep target')
        continue

    source_chunks[:len(real_chunks)] = real_chunks

    target_dir = os.path.dirname('/'.join(source_chunks))
    os.makedirs(target_dir, exist_ok=True)
    if not args.copy:
        print('Moving', filename, 'to', target_dir)
        shutil.move(filename, target_dir)
    else:
        print('Copying', filename, 'to', target_dir)
        if os.path.isdir(filename):
            shutil.copytree(filename, os.path.join(target_dir, filename))
        else:
            shutil.copy(filename, target_dir)
