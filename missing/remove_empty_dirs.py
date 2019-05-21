#!/usr/bin/env python

from __future__ import print_function

from collections import deque

import argparse
import os

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x

EXCLUSIONS = ['.git']


class Node:
    path = ''
    parent = None
    files = 0
    subdirs = 0
    subdirs_left = 0

    def __str__(self):
        return '{} : {} files, {} subdirectories'.format(self.path, self.files, self.subdirs)


class PrintHandler:
    def handle(self, node):
        print(node)
        return False

    def close(self):
        pass


class RemoveDirHandler:
    def __init__(self):
        self.log = open('removed_directories.txt', 'a')

    def handle(self, node):
        if any(exclusion in node.path for exclusion in EXCLUSIONS):
            print('Not removing (excluded):', node.path)
            return False

        print('Removing:', node.path)
        os.rmdir(node.path)

        if self.log:
            self.log.write(node.path)
            self.log.write('\n')

        return True

    def close(self):
        if self.log:
            self.log.close()
            self.log = None


def remove_from_parent(filesystem, node, new_leaves):
    parent = filesystem.get(node.parent)
    if parent is None:
        return

    parent.subdirs_left -= 1
    if parent.subdirs_left == 0 and parent.files == 0:
        new_leaves.append(parent)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rmdir', '-x', action='store_true', help='remove empty directories and log')
    args = parser.parse_args()

    filesystem = {}
    leaves = []
    handler = RemoveDirHandler() if args.rmdir else PrintHandler()

    for path, subdirs, files in tqdm(os.walk('.')):
        if path == '.':
            # we'll not delete CWD anyway
            continue

        node = Node()
        node.path = path
        node.parent = os.path.dirname(path)
        node.files = len(files)
        node.subdirs = node.subdirs_left = len(subdirs)

        filesystem[path] = node

        if node.files == 0 and node.subdirs == 0:
            leaves.append(node)


    new_leaves = deque()
    count = len(leaves)
    removed = 0

    print('Empty directories: ({})'.format(count))
    for node in leaves:
        removed += handler.handle(node)
        remove_from_parent(filesystem, node, new_leaves)

    if new_leaves:
        print('Recursively empty directories:')

    while new_leaves:
        node = new_leaves.popleft()
        removed += handler.handle(node)
        remove_from_parent(filesystem, node, new_leaves)
        count += 1

    handler.close()
    print('{} total empty directories'.format(count))
    if args.rmdir:
        print('{} total directories removed'.format(removed))


if __name__ == '__main__':
    main()
