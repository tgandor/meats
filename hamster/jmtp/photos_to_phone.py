#!/usr/bin/env python

import glob
import json
import os
# import shutil
import time

photos_card = '/mnt/extSdCard/DCIM/Camera'
photos_phone = '/mnt/sdcard/DCIM/Camera'

MB = 2**20
size_limit = 2500 * MB

copied_json = os.path.join(os.path.dirname(__file__), 'copied.json')

if os.path.exists(copied_json):
    already = set(json.load(open(copied_json)))
else:
    already = set()

files = list(sorted(glob.glob(os.path.join(photos_card, '*'))))
target_dir = photos_phone

files_to_download = [f for f in files if not os.path.exists(os.path.join(target_dir, os.path.basename(f))) and f not in already]
to_download = len(files_to_download)
print("{} total files, {} left to download.".format(len(files), to_download))

i = total_size = 0
start_all = time.time()
for f in files_to_download:
    start_single = time.time()
    size = os.path.getsize(f)
    if total_size + size > size_limit:
        print("Size limit reached.")
        break
    os.system('cp "{}" "{}"'.format(f, photos_phone))
    already.add(f)
    elapsed = time.time() - start_single
    i += 1
    total_size += size
    print("Copied {} ({:,} KB) in {:.1f}s ({:.1f} KB/s). {}/{}".format(os.path.basename(f), size/1024, elapsed, size / elapsed / 1024, i, to_download))

elapsed = time.time() - start_all
size = total_size

print("Copied {} files ({:,} MB total) in {:.1f}s ({:.1f} KB/s).".format(i, size/1024/1024, elapsed, size / elapsed / 1024))

with open(copied_json, 'w') as f:
    print("{} files copied already".format(len(already)))
    json.dump(list(sorted(already)), f, indent=4)

os.system("df -h " + photos_phone)
