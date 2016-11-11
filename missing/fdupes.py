#!/usr/bin/env python

import hashlib
import itertools
import os
import sys
import time
from threading import Event, Thread

# config / flags
do_delete = False


def md5sum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as fileobj:
        for chunk in iter(lambda: fileobj.read(2**12), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def suitability_max_len_penalize_spaces(x):
    return -len(x.replace(' ', '').replace('(', '').replace(')', ''))


def call_repeatedly(interval, func):
    stopped = Event()
    def loop():
        ctr = 0
        while not stopped.wait(interval): # the first call is in `interval` secs
            ctr += 1
            func(ctr)
    Thread(target=loop).start()
    return stopped.set


def show_update(since, dirs, files, ctr):
    sys.stdout.write('Processing... {} {:.1f} s ({} dirs, {} files)\r'.format(
        '|/-\\'[ctr % 4], time.time()-since, dirs, len(files)))
    sys.stdout.flush()


if '-d' in sys.argv[1:]:
    do_delete = True

files = []
dirs = 0
walk_start = time.time()

cancel_update = call_repeatedly(1.0, lambda ctr: show_update(walk_start, dirs, files, ctr))

try:
    for dirpath, dirnames, filenames in os.walk('.'):
        dirs += 1
        for f in filenames:
            filename = os.path.join(dirpath, f)
            if os.path.islink(filename):
                continue
            try:
                t = (md5sum(filename), os.stat(filename).st_size, filename)
                files.append(t)
            except IOError:
                sys.stderr.write('IOError: {}\n'.format(filename))
finally:
    cancel_update()

processing_start = time.time()
print('Done in {:.1f} s. ({} dirs, {} files){}'.format(
    time.time() - walk_start, dirs, len(files), ' '*32))

total_waste = 0
total_by4kb = 0
total_files = 0

groups = []

for (md5, size), dup_files in itertools.groupby(sorted(files), lambda t: t[:2]):
    group = list(dup_files)
    # print(md5, group)
    if len(group) == 1:
        continue

    # some statistics
    total_files += len(group)-1
    total_waste += (len(group)-1) * size
    total_by4kb += ((len(group)-1) * size + 2**12 - 1) // (2**12)

    filenames = sorted((g[2] for g in group), key = suitability_max_len_penalize_spaces)
    groups.append((md5, size, filenames))

groups.sort(key=lambda x: x[1] * (len(x[2]) - 1))
group_count = 0

for md5, size, filenames in groups:
    group_count += 1
    print('{}. {} {}\n{}\n'.format(group_count, md5, size, '\n'.join(filenames)))

    if do_delete:
        if size == 0:
            print('Not deleting empty files.')
            continue
        for f in filenames[1:]:
            os.unlink(f)

print('Total waste: {:,} Bytes; {:,} KB (4KB-blocks) in {} extra files.'.format(
    total_waste, total_by4kb * 4, total_files))

print('Processed in {:.1f} s. ({:.1f} s total)'.format(
    time.time() - processing_start, time.time() - walk_start))
