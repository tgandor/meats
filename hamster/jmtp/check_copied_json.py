#!/usr/bin/env python

import glob
import json
import os
import sys

if len(sys.argv) < 3:
    print("Usage: {} PHOTOS_JSON TARGET_DIR...".format(sys.argv[0]))
    exit()

json_file = sys.argv[1]

if not os.path.exists(json_file):
    print("photos.json file must exist")
    exit()

files = json.load(open(json_file))
print("{} files in JSON.".format(len(files)))

all_target_files = set()
for target_dir in sys.argv[2:]:
    if not os.path.isdir(target_dir):
        print("{} is not a directory".format(target_dir))
        exit()
    target_files = set(map(os.path.basename, glob.glob(os.path.join(target_dir, '*'))))
    print("{} files in {}".format(len(target_files), target_dir))
    all_target_files |= target_files

print("{} files altogether.".format(len(all_target_files), target_dir))

files_copied = [f for f in files
    if os.path.basename(f) in all_target_files]

if len(files_copied) < len(files):
    print("Error: missing {} files:".format(len(files)-len(files_copied)))
    for f in sorted(set(files) - set(files_copied)):
        print(f)

