#!/usr/bin/env python

import glob
import os
import shutil
import sys
import time

if len(sys.argv) < 3:
    print("Usage: {} SOURCE_DIR TARGET_DIR".format(sys.argv[0]))
    exit()

source_dir = sys.argv[1]

if not os.path.isdir(source_dir):
    print("{} is not a directory".format(source_dir))
    exit()

target_dir = sys.argv[2]

if not os.path.isdir(target_dir):
    print("{} is not a directory".format(target_dir))
    exit()

files = sorted(glob.glob(os.path.join(source_dir, '*')))

files_to_download = [f for f in files if not os.path.exists(os.path.join(target_dir, os.path.basename(f)))]

to_download = len(files_to_download)
print("{} total files, {} left to download.".format(len(files), to_download))

i = total_size = 0
start_all = time.time()
for f in files_to_download:
    start_single = time.time()
    base_name = os.path.basename(f)
    print("{}...".format(base_name))
    target_file = os.path.join(target_dir, base_name)
    shutil.move(f, target_file)
    size = os.path.getsize(target_file)
    elapsed = time.time() - start_single
    i += 1
    total_size += size
    print("Copied {} ({:,} KB) in {:.1f}s ({:.1f} KB/s). {}/{}".format(base_name, size/1024, elapsed, size / elapsed / 1024, i, to_download))

elapsed = time.time() - start_all
size = total_size
print("Copied {} files ({:,} MB total) in {:.1f}s ({:.1f} KB/s).".format(i, size/1024/1024, elapsed, size / elapsed / 1024))
