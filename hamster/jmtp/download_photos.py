#!/usr/bin/env python

import json
import os
import shutil
import sys
import time

if len(sys.argv) < 3:
    print("Usage: {} PHOTOS_JSON TARGET_DIR".format(sys.argv[0]))
    exit()

json_file = sys.argv[1]

if not os.path.exists(json_file):
    print("photos.json file must exist")
    exit()

target_dir = sys.argv[2]

if not os.path.isdir(target_dir):
    print("{} is not a directory".format(target_dir))
    exit()

files = json.load(open(json_file))

files_to_download = [f for f in files if not os.path.exists(os.path.join(target_dir, os.path.basename(f)))]

to_download = len(files_to_download)
print("{} total files, {} left to download.".format(len(files), to_download))

i = total_size = 0
start_all = time.time()
for f in files_to_download:
    start_single = time.time()
    shutil.copy(str(f), target_dir)
    size = os.path.getsize(os.path.join(target_dir, os.path.basename(f)))
    elapsed = time.time() - start_single
    i += 1
    total_size += size
    print("Copied {} ({:,} KB) in {:.1f}s ({:.1f} KB/s). {}/{}".format(os.path.basename(f), size/1024, elapsed, size / elapsed / 1024, i, to_download))

elapsed = time.time() - start_all
size = total_size
print("Copied {} files ({:,} MB total) in {:.1f}s ({:.1f} KB/s).".format(i, size/1024/1024, elapsed, size / elapsed / 1024))
