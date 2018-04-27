#!/usr/bin/env python

import argparse
import hashlib
import itertools
import json
import os
import sys
import time
from operator import attrgetter
from threading import Event, Thread

parser = argparse.ArgumentParser()
parser.add_argument('--delete', '-d', action='store_true', help='Delete the duplicates')
parser.add_argument('--basename', '-n', action='store_true', help='Group by basename (first)')
parser.add_argument('--basename-only', '-N', action='store_true', help='Group by basename (only)')
args = parser.parse_args()


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
        while not stopped.wait(interval):  # the first call is in `interval` secs
            ctr += 1
            func(ctr)
    Thread(target=loop).start()
    return stopped.set


def show_update(since, dirs, files, ctr):
    sys.stdout.write('Processing... {} {:.1f} s ({} dirs, {} files)\r'.format(
        '|/-\\'[ctr % 4], time.time()-since, dirs, len(files)))
    sys.stdout.flush()


class lazy_property(object):
    """
    meant to be used for lazy evaluation of an object attribute.
    property should represent non-mutable data, as it replaces itself.

    https://stackoverflow.com/a/6849299/1338797
    """

    def __init__(self, fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value


class File:
    def __init__(self, filepath, filename):
        self.basename = filename
        self.filepath = filepath
        self.size = os.stat(filepath).st_size

    def __repr__(self):
        return 'File({}; {:,} B; {})'.format(self.filepath, self.size, self.md5)

    @lazy_property
    def md5(self):
        return md5sum(self.filepath)

    def as_dict(self):
        return {'filepath': self.filepath, 'filename': self.basename, 'size': self.size, 'md5': self.md5}


def group_files(files, key=attrgetter('basename')):
    for key_value, group in itertools.groupby(sorted(files, key=key), key):
        candidate = list(group)
        if len(candidate) > 1:
            yield candidate


def process_groups(group_list):
    for group in group_list:
        print(group[0].basename)
        for file in group:
            print(file)
        print('-' * 20)

    if len(groups) == 0:
        print('No duplicates found.')


def save_groups(group_list):
    if len(group_list) == 0:
        print('Not saving empty groups.')
        return

    json_dump = 'fdupes_groups_{}.json'.format(time.strftime('%Y%m%d_%H%M%S'))
    with open(json_dump, 'w') as dump:
        json.dump([
            [file.as_dict() for file in group]
            for group in group_list
        ], dump, indent=2)
    print('Groups saved in:', json_dump)


all_files = []
dirs = 0
walk_start = time.time()

cancel_update = call_repeatedly(1.0, lambda ctr: show_update(walk_start, dirs, all_files, ctr))

try:
    for dirpath, dirnames, filenames in os.walk('.'):
        dirs += 1
        for f in filenames:
            filename = os.path.join(dirpath, f)
            if os.path.islink(filename):
                continue
            try:
                all_files.append(File(filename, f))
            except IOError:
                sys.stderr.write('IOError: {}\n'.format(filename))
finally:
    cancel_update()

processing_start = time.time()
print('Done in {:.1f} s. ({} dirs, {} files){}'.format(
    time.time() - walk_start, dirs, len(all_files), ' '*32))

total_waste = 0
total_by4kb = 0
total_files = 0

if args.basename or args.basename_only:
    groups = list(group_files(all_files))
    print('After grouping by basename: {} groups'.format(len(groups)))
else:
    groups = [all_files]

if not args.basename_only:
    groups = [new_group for group in groups for new_group in group_files(group, key=attrgetter('size'))]
    print('After grouping by size: {} groups'.format(len(groups)))
    groups = [new_group for group in groups for new_group in group_files(group, key=attrgetter('md5'))]
    print('After grouping by md5: {} groups'.format(len(groups)))

process_groups(groups)
save_groups(groups)

'''
if len(groups) > 0:
    json_dump = 'fdupes_groups.json'
    suffix = 0
    while os.path.exists(json_dump):
        suffix += 1
        json_dump = 'fdupes_groups_{}.json'.format(suffix)

    with open(json_dump, 'w') as dump:
        json.dump(groups, dump, indent=2)

    for md5, size, filenames in groups:
        group_count += 1
        print('{}. {} {}\n{}\n'.format(group_count, md5, size, '\n'.join(filenames)))

        if args.delete:
            if size == 0:
                print('Not deleting empty files.')
                continue
            for f in filenames[1:]:
                os.unlink(f)

    print('Total waste: {:,} Bytes; {:,} KB (4KB-blocks) in {} extra files.'.format(
        total_waste, total_by4kb * 4, total_files))
else:
    print('No duplicates found.')
'''

print('Processed in {:.1f} s. ({:.1f} s total)'.format(
    time.time() - processing_start, time.time() - walk_start))
