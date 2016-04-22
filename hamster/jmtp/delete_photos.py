#!/usr/bin/env python

import json
import os
import sys
import time

if len(sys.argv) < 2:
    print("Usage: {} PHOTOS_JSON".format(sys.argv[0]))
    exit()

json_file = sys.argv[1]

if not os.path.exists(json_file):
    print("photos.json file must exist")
    exit()

files = json.load(open(json_file))
to_delete = len(files)

print("{} total files.".format(to_delete))

i = total_size = 0
start_all = time.time()
for f in files:
    size = os.path.getsize(f)
    os.remove(str(f))
    i += 1
    total_size += size
    print("Deleted {} ({:,} KB) {}/{}".format(os.path.basename(f), size/1024, i, to_delete))

elapsed = time.time() - start_all
size = total_size
print("Deleted {} files ({:,} MB total) in {:.1f}s ({:.1f} KB/s).".format(i, size/1024/1024, elapsed, size / elapsed / 1024))
