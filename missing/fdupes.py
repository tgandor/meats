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

print('Done in {:.1f} s. ({} dirs, {} files){}'.format(
    time.time() - walk_start, dirs, len(files), ' '*32))

for (md5, size), dup_files in itertools.groupby(sorted(files), lambda t: t[:2]):
    group = list(dup_files)
    # print(md5, group)
    if len(group) == 1:
        continue
    filenames = sorted((g[2] for g in group), key = suitability_max_len_penalize_spaces)
    print('{} {}\n{}\n'.format(md5, size, '\n'.join(filenames)))

    if do_delete:
        for f in filenames[1:]:
            os.unlink(f)
