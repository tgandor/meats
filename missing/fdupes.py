#!/usr/bin/env python

from __future__ import print_function

import argparse
import hashlib
import itertools
import json
import os
import sys
import time
from operator import attrgetter
from threading import Event, Thread


def md5sum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as fileobj:
        for chunk in iter(lambda: fileobj.read(2**12), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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
    def __init__(self, file_path):
        self.file_path = file_path

    def __repr__(self):
        return 'File({})'.format(self.file_path)

    @lazy_property
    def basename(self):
        return os.path.basename(self.file_path)

    @lazy_property
    def size(self):
        try:
            return os.stat(self.file_path).st_size
        except IOError:
            return -1

    @lazy_property
    def md5(self):
        return md5sum(self.file_path)

    def as_dict(self):
        return {'path': self.file_path}

    @staticmethod
    def from_dict(data):
        return File(data['path'])


def suitability_max_len_penalize_spaces(file_):
    """
    Key function for files, negative length with spaces and parentheses removed.
    :param file_: `File` file object to evaluate
    :return: `int` suitability score
    """
    return -len(file_.file_path.replace(' ', '').replace('(', '').replace(')', ''))


class Group:
    def __init__(self, files, features={}):
        self.files = files
        self.features = features

    def __len__(self):
        return len(self.files)

    def __getitem__(self, item):
        return self.files[item]

    def __getattr__(self, item):
        try:
            return self.features[item]
        except KeyError as keyError:
            raise AttributeError(keyError.args)

    def __repr__(self):
        return 'Group({}, {})'.format(self.features, self.files)

    def as_dict(self):
        return {
            'features': self.features,
            'files': [file.as_dict() for file in self.files]
        }

    @staticmethod
    def load(filename):
        with open(filename) as stream:
            data = json.load(stream)

        group = Group(data['files'], data['features'])
        return group


def group_files(files, attr='basename'):
    """
    Group files into lists with identical value of attr.
    :param files: Union[List[File], Group] list of files to sort
    :param attr: str Attribute to group by the files
    :return: Generator[List[File]]

    >>> list(group_files([]))
    []
    >>> list(group_files([File('a/b'), File('c/b')]))
    [Group({'basename': 'b'}, [File(a/b), File(c/b)])]
    """
    key = attrgetter(attr)
    features = files.features if hasattr(files, 'features') else {}
    for key_value, group in itertools.groupby(sorted(files, key=key), key):
        candidate = list(group)
        if len(candidate) > 1:
            new_features = features.copy()
            new_features[attr] = key_value
            yield Group(candidate, new_features)


def regroup(group_list, attr='basename'):
    """
    Group all lists by attribute `attr` and return a list of the nen groups.
    :param attr: str name of file attribute to use for regrouping
    :type group_list: List[Group]
    :rtype: List[Group]
    """
    return [new_group for group in group_list for new_group in group_files(group, attr=attr)]


def group_summary(group):
    if hasattr(group, 'size'):
        return 'files: {}, waste: {:,} B'.format(len(group), group_waste(group))
    else:
        return 'files: {}'.format(len(group))


def process_groups(group_list):
    for group in group_list:
        print(group.features)
        for file in group:
            print(file)
        print('-' * 20, group_summary(group), '-' * 20)


def _as_dict(group):
    if hasattr(group, 'as_dict'):
        return group.as_dict()
    return [file.as_dict() for file in group]


def group_total(group):
    return len(group) * group.size


def group_waste(group):
    return (len(group) - 1) * group.size


def groups_summary(groups):
    return '{:,} groups, {:,} files, {:,} B total, {:,} B waste'.format(
        len(groups),
        sum(map(len, groups)),
        sum(map(group_total, groups)),
        sum(map(group_waste, groups))
    )


def sort_members(group, key=suitability_max_len_penalize_spaces):
    """
    Sort files inside group by some criterion.
    :param key: Callable[[File], Any]
    :type group: Group
    """
    group.files.sort(key=key)


def save_groups(group_list, prefix=''):
    if len(group_list) == 0:
        print('Not saving empty groups.')
        return

    print('Saving {} groups...'.format(len(group_list)))
    json_dump = prefix + 'fdupes_groups_{}.json'.format(time.strftime('%Y%m%d_%H%M%S'))
    with open(json_dump, 'w') as dump:
        json.dump([_as_dict(group) for group in group_list], dump, indent=2)
    print('Groups saved in:', json_dump)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--delete', '-d', action='store_true', help='Delete the duplicates')
    parser.add_argument('--basename', '-n', action='store_true', help='Group by basename (first)')
    parser.add_argument('--basename-only', '-N', action='store_true', help='Group by basename (only)')
    parser.add_argument('--no-md5', '-5', action='store_true', help='Skip grouping by md5 sum')
    parser.add_argument('--no-print', '-P', action='store_true', help='Skip printing the groups')
    parser.add_argument('--no-save', '-S', action='store_true', help='Skip saving the groups as JSON')
    parser.add_argument('--prefix', '-p', help='Prefix for saving the groups', default='')
    parser.add_argument('directories', nargs='*', help='Directories to scan for duplicates', default=['.'])
    return parser.parse_args()


def main():
    args = parse_args()

    all_files = []
    dirs = 0
    walk_start = time.time()

    cancel_update = call_repeatedly(1.0, lambda ctr: show_update(walk_start, dirs, all_files, ctr))
    try:
        for directory in args.directories:
            for dirpath, dirnames, filenames in os.walk(directory   ):
                dirs += 1
                for f in filenames:
                    filename = os.path.join(dirpath, f)
                    if os.path.islink(filename):
                        continue
                    all_files.append(File(filename))
    finally:
        cancel_update()

    processing_start = time.time()
    print('Done in {:.1f} s. ({} dirs, {} files){}'.format(
        time.time() - walk_start, dirs, len(all_files), ' '*32))

    if args.basename or args.basename_only:
        groups = list(group_files(all_files))
        print('After grouping by basename: {} groups'.format(len(groups)))
    else:
        groups = [all_files]

    if not args.basename_only:
        groups = regroup(groups, 'size')
        print('After grouping by size: ' + groups_summary(groups))
        if not args.no_md5:
            groups = regroup(groups, 'md5')
            print('After grouping by md5: ' + groups_summary(groups))

    if len(groups) == 0:
        print('No duplicate groups found.')
        exit()

    if any(hasattr(group, 'size') for group in groups):
        groups.sort(key=group_waste)
    else:
        groups.sort(key=len)

    for group in groups:
        sort_members(group)

    if not args.no_print:
        process_groups(groups)

    if not args.no_save:
        save_groups(groups, args.prefix)

    if args.delete:
        pass

    print('Processed in {:.1f} s. ({:.1f} s total)'.format(
        time.time() - processing_start, time.time() - walk_start))


if __name__ == '__main__':
    main()
