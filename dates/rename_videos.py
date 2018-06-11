#!/usr/bin/env python

# very rudimentary

import argparse
import os
import glob
import itertools
import sys

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--player', default='mplayer')
args = parser.parse_args()

# queue = []
event_name = ''
event_date = None


def get_date(name):
    return name[:4] + '-' + name[4:6] + '-' + name[6:8]


def move(name, target_directory):
    print('Renaming {} into {}'.format(name, target_directory))
    if not os.path.isdir(target_directory):
        os.makedirs(target_directory)
    os.rename(name, os.path.join(target_directory, name))


for filename in sorted(itertools.chain.from_iterable(map(glob.glob, args.files))):
    os.system(args.player + ' ' + filename)

    print('Event name (empty = {})'.format(event_name))

    answer = sys.stdin.readline().strip()
    if answer:
        event_name = answer.replace(' ', '-')
        event_date = None

    if not event_date:
        event_date = get_date(filename)

    move(filename, event_date + '-' + event_name)
