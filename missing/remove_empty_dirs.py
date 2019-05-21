#!/usr/bin/env python

from __future__ import print_function

from collections import deque

import os

EXCLUSIONS = ['.git']


class Node:
    path = ''
    parent = None
    files = 0
    subdirs = 0
    subdirs_left = 0

    def __str__(self):
        return '{} : {} files, {} subdirectories'.format(self.path, self.files, self.subdirs)


filesystem = {}
leaves = []

for path, subdirs, files in os.walk('.'):
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

    # print(node)


def remove_from_parent(filesystem, node, new_leaves):
    parent = filesystem.get(node.parent)
    if parent is None:
        return

    parent.subdirs_left -= 1
    if parent.subdirs_left == 0:
        new_leaves.append(parent)


new_leaves = deque()

print('Empty directories:')
for node in leaves:
    print(node.path)
    remove_from_parent(filesystem, node, new_leaves)

if new_leaves:
    print('Recursively empty directories:')

while new_leaves:
    node = new_leaves.popleft()
    print(node)
    remove_from_parent(filesystem, node, new_leaves)
