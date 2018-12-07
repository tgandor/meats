#!/usr/bin/env python

from __future__ import print_function

import argparse
import hashlib
import itertools
import json
import logging
import os
import sys
import time
from operator import attrgetter
from threading import Event, Thread


def md5sum(filename, chunk_size=2**12):
    logging.getLogger().debug('MD5 %s', filename)
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def call_repeatedly(interval, func):
    stopped = Event()

    def loop():
        ctr = 0
        while not stopped.wait(interval):  # the first call is in `interval` secs
            ctr += 1
            func(ctr)
    thread = Thread(target=loop)
    thread.daemon = True  # be careful whan interrupting while processing...
    thread.start()
    return stopped.set


class LazyProperty(object):
    """
    meant to be used for lazy evaluation of an object attribute.
    property should represent non-mutable data, as it replaces itself.

    https://stackoverflow.com/a/6849299/1338797
    """

    def __init__(self, real_getter):
        self.real_getter = real_getter
        self.attribute_name = real_getter.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.real_getter(obj)
        setattr(obj, self.attribute_name, value)
        return value


class File:
    def __init__(self, file_path):
        self.file_path = file_path

    def __repr__(self):
        return 'File({})'.format(self.file_path)

    def __lt__(self, other):
        return self.file_path < other.file_path

    @LazyProperty
    def basename(self):
        return os.path.basename(self.file_path)

    @LazyProperty
    def size(self):
        try:
            return os.stat(self.file_path).st_size
        except IOError:
            return -1

    @LazyProperty
    def md5(self):
        return md5sum(self.file_path)

    def as_dict(self):
        result = self.__dict__.copy()
        all_keys = list(result.keys())
        for key in all_keys:
            if hasattr(result[key], 'real_getter'):
                del result[key]
        return result

    @staticmethod
    def from_dict(data):
        return File(data['path'])


def custom_dumper(obj):
    if hasattr(obj, 'as_dict'):
        return obj.as_dict()
    return obj.__dict__


def suitability_max_len_penalize_spaces(file_):
    """
    Key function for files, negative length with spaces and parentheses removed.
    :param file_: `File` file object to evaluate
    :return: `int` suitability score
    """
    return -len(file_.file_path.replace(' ', '').replace('(', '').replace(')', '')), file_.file_path


class Group:
    def __init__(self, files, features=None):
        self.files = files
        self.features = features or dict()

    def __len__(self):
        return len(self.files)

    def __getitem__(self, item):
        return self.files[item]

    def __getattr__(self, item):
        try:
            return self.features[item]
        except KeyError as keyError:
            # below seemed a good idea, but is fatal:
            # if item == 'size': return float('nan')
            raise AttributeError(keyError.args)

    def __repr__(self):
        return 'Group({}, {})'.format(self.features, sorted(self.files))

    def as_dict(self):
        return {
            'features': self.features,
            'files': [file.as_dict() for file in sorted(self.files)]
        }


def group_files(files, attr='basename', out_unique=None):
    """
    Group files into lists with identical value of attr.
    :param files: Union[List[File], Group] list of files to sort
    :param attr: str Attribute to group by the files
    :param out_unique: List[File] output argument for unique files discarded in regroup
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
            # print('new features:', new_features)
            yield Group(candidate, new_features)
        elif out_unique is not None:
            out_unique.extend(candidate)


def regroup(group_list, attr='basename', out_unique=None):
    """
    Group all lists by attribute `attr` and return a list of the new groups.
    :param attr: str name of file attribute to use for regrouping
    :type group_list: List[Group]
    :param out_unique: List[File] output argument for unique files discarded in regroup
    :rtype: List[Group]
    """

    def show_update(since, worked, total, ctr):
        sys.stdout.write('Processing... {} {}/{} {:.1f} s\r'.format(
            '|/-\\'[ctr % 4], worked, total, time.time() - since))
        sys.stdout.flush()


    def _regroup():
        for group in group_list:
            done[0] += 1

            if hasattr(group, attr):
                yield group
                continue

            for new_group in group_files(group, attr=attr, out_unique=out_unique):
                yield new_group

    done = [0]
    start = time.time()
    total = len(group_list)

    cancel = call_repeatedly(1.0, lambda ctr: show_update(start, done[0], total, ctr))
    new_groups = list(_regroup())
    cancel()
    print()

    print('After grouping by {}: {}'.format(attr, groups_summary(new_groups)))
    return new_groups


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
    if len(groups) == 0:
        return '0 groups'

    if not hasattr(groups[0], 'size'):
        return '{:,} groups, {:,} files, size and waste unknown'.format(
            len(groups),
            sum(map(len, groups)),
        )

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


def save_groups(group_list, prefix='', unique_files=None):
    if len(group_list) == 0:
        print('Not saving empty groups.')
        return

    print('Saving {} groups and {} unique files...'.format(len(group_list), len(unique_files or [])))
    json_dump = prefix + 'fdupes_groups_{}.json'.format(time.strftime('%Y%m%d_%H%M%S'))
    with open(json_dump, 'w') as dump:
        json.dump({
            'groups': [_as_dict(group) for group in group_list],
            'unique': unique_files
        }, dump, default=custom_dumper, indent=2)
    print('Groups saved in:', json_dump)


def load_groups(filename):
    with open(filename) as stream:
        data = json.load(stream)

    groups = [Group([File(file_dict['path']) for file_dict in group_dict['files']],
                    group_dict['features'])
              for group_dict in data['groups']]
    return groups


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--basename', '-n', action='store_true', help='Group by basename (first)')
    parser.add_argument('--basename-only', '-N', action='store_true', help='Group by basename (only)')
    parser.add_argument('--debug', '-v', action='store_true', help='Show verbose debugging output')
    parser.add_argument('--delete', '-d', action='store_true', help='Delete the duplicates interactively')
    parser.add_argument('--delete-command', help='Use a different command to delete duplicates, e.g. "git rm"')
    parser.add_argument('--delete-now', '-D', action='store_true', help='Delete the duplicates automatically')
    parser.add_argument('--groups', '-i', help='Saved group files to load instead of scanning')
    parser.add_argument('--hardlink', '-H', action='store_true', help='Hardlink the duplicate files')
    parser.add_argument('--min-size', '-m', help='Min size in B of deleted files (auto mode)', type=int, default=1)
    parser.add_argument('--no-md5', '-5', action='store_true', help='Skip grouping by md5 sum')
    parser.add_argument('--no-print', '-P', action='store_true', help='Skip printing the groups')
    parser.add_argument('--no-save', '-S', action='store_true', help='Skip saving the groups as JSON')
    parser.add_argument('--prefix', '-p', help='Prefix for saving the groups', default='')
    parser.add_argument('--unique', '-u', action='store_true', help='Keep track of unique files')
    parser.add_argument('directories', nargs='*', help='Directories to scan for duplicates', default=['.'])
    return parser.parse_args()


class Profiler:
    def __init__(self):
        self.times = [time.time()]

    def finish_phase(self, phase=None):
        self.times.append(time.time())
        print('Finished {} in {:.1f} s. ({:.1f} s total)'.format(
            phase or '',
            self.times[-1] - self.times[-2],
            self.times[-1] - self.times[0]))


def delete_interactive(groups):
    for group in groups[::-1]:
        print(group.features)
        for i, file_ in enumerate(group.files):
            print(i, file_)
        print(group_summary(group))
        print('Which file to preserve (0-{}, a - all, q - quit)?'.format(len(group) - 1))
        answer = sys.stdin.readline().strip()
        if answer == 'q':
            break
        if answer in ('a', ''):
            continue
        idx = int(answer)
        for i, file_ in enumerate(group.files):
            if i == idx:
                continue
            os.unlink(file_.file_path)


def delete_unattended(groups, args):
    """
    Delete non-first files from every group, no smaller than min_size.

    :param groups: List[Group]
    :param args.min_size: int smallest size of deleted duplicate in bytes
    :param args.delete_command: Optional[str] command to use in lieu of os.unlink
    :return: List[Group] groups which where not deleted due to size.
    """
    print('Deleting up to {} groups:'.format(len(groups)))
    groups.sort(key=attrgetter('size'))  # stabilizing min_size

    total_cleared = 0
    iterator = iter(groups[::-1])
    for group in iterator:
        print(group.features)
        ensure_deletable(group)
        if group.size < args.min_size:
            print('Size limit ({}) reached.'.format(args.min_size))
            return list(iterator)

        for i, file_ in enumerate(group.files):
            if not os.path.exists(file_.file_path):
                print('Critical: {} not found'.format(file_.file_path))
                raise ValueError('One of group files does not exist')

            if i == 0:
                print('Leaving behind:', file_.file_path)
                continue

            print('Deleting:', file_.file_path)
            if args.delete_command:
                os.system('{} "{}"'.format(args.delete_command, file_.file_path))
            else:
                os.unlink(file_.file_path)

        waste = group_waste(group)
        total_cleared += waste
        print('--- {:,} B cleared ({:,} B total) ---'.format(waste, total_cleared))
    return []


def ensure_deletable(group):
    if not hasattr(group, 'size') or not hasattr(group, 'md5'):
        raise ValueError('Group is not specific enough for members to be safely deleted')


def link_groups_hard(groups):
    for group in groups:
        ensure_deletable(group)
        single = group[0] # type: File
        if not os.path.exists(single.file_path):
            raise ValueError('Main file of group ({}) not found'.format(single.file_path))

        print('Leaving behind:', single.file_path)

        for file_ in group[1:]: # type: File
            if not os.path.exists(file_.file_path):
                raise ValueError('A file in group ({}) not found'.format(single.file_path))
            print('Relinking:', file_.file_path)
            os.unlink(file_.file_path)
            os.link(single.file_path, file_.file_path)


def main():
    args = parse_args()
    profiler = Profiler()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.groups:
        groups = load_groups(args.groups)
        profiler.finish_phase('loading groups')
    else:
        all_files = scan_directories(args)
        groups = [Group(all_files)]
        profiler.finish_phase('scanning directories')

    unique_files = [] if args.unique else None

    if args.basename or args.basename_only:
        groups = regroup(groups, out_unique=unique_files)

    if not args.basename_only:
        groups = regroup(groups, 'size', unique_files)
        if not args.no_md5:
            groups = regroup(groups, 'md5', unique_files)

    profiler.finish_phase('grouping files')

    if len(groups) == 0:
        print('No duplicate groups found.')
        if unique_files:
            print('{} unique files found.'.format(len(unique_files)))
        exit()

    sort_groups(groups)

    if not args.no_print:
        process_groups(groups)
        profiler.finish_phase('printing groups')

    if not args.no_save:
        save_groups(groups, args.prefix, unique_files)
        profiler.finish_phase('saving groups')

    if args.delete:
        delete_interactive(groups)
        profiler.finish_phase('interactive processing')
    elif args.delete_now:
        rest = delete_unattended(groups, args)
        if rest:
            print('Remaining groups:', groups_summary(rest))
            save_groups(rest, args.prefix + 'left_')
        profiler.finish_phase('deleting duplicates')
    elif args.hardlink:
        link_groups_hard(groups)


def scan_directories(args):
    def show_update(since, dirs, files, ctr):
        sys.stdout.write('Processing... {} {:.1f} s ({} dirs, {} files)\r'.format(
            '|/-\\'[ctr % 4], time.time() - since, dirs, len(files)))
        sys.stdout.flush()

    all_files = []
    dirs = 0
    walk_start = time.time()
    cancel_update = call_repeatedly(1.0, lambda ctr: show_update(walk_start, dirs, all_files, ctr))
    try:
        for directory in args.directories:
            for dir_path, dir_names, filenames in os.walk(directory):
                logging.getLogger().debug('Processing directory: %s', dir_path)
                dirs += 1
                for f in filenames:
                    logging.getLogger().debug('File: %s', f)
                    filename = os.path.join(dir_path, f)
                    if os.path.islink(filename):
                        continue
                    all_files.append(File(filename))
    finally:
        cancel_update()

    return all_files


def sort_groups(groups):
    if any(hasattr(group, 'size') for group in groups):
        groups.sort(key=group_waste)
    else:
        groups.sort(key=len)
    for group in groups:
        sort_members(group)


if __name__ == '__main__':
    main()
