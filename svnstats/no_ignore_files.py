#!/usr/bin/env python

import os

def get_alien_files__pipe():
    for line in os.popen('svn st --no-ignore'):
        if not line.strip():
            continue
        st, filename = line.split(None, 1)
        if st in 'I?':
            yield filename.strip()

def get_alien_files__entries(top='.'):
    from os.path import join, isdir, exists, islink
    entries_file = join(top, '.svn/entries')
    if not exists(entries_file):
        # print 'Not exists:', entries_file
        return
    # print 'Entering', top
    entries = open(entries_file).read().split('\x0c\n')
    versioned = set(entry.split('\n', 1)[0] for entry in entries[1:-1])
    present = set(os.listdir(top)) - set(['.svn'])
    if top == '.':
        top = ''
    for non_versioned in present - versioned:
        candidate = join(top, non_versioned)
        if isdir(candidate) and not islink(candidate) and exists(join(candidate, '.svn')):
            # caveat: this is an external working copy
            continue
        yield candidate
    for entry in versioned:
        maybe_subdir = join(top, entry)
        if isdir(maybe_subdir):
            for alien in get_alien_files__entries(maybe_subdir):
                yield alien

def test():
    # print 'pipe:', sorted(get_alien_files__pipe())[:10]
    # print 'entries:', sorted(get_alien_files__entries())[:10]
    entries = set(get_alien_files__entries())
    pipe = set(get_alien_files__pipe())
    print 'Not in pipe:', entries-pipe
    print 'Not in entrie:', pipe-entries

for filename in get_alien_files__entries():
    print filename
