#!/usr/bin/env python

# very rudimentary

import argparse
import glob
import itertools
import os
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--player', default='mplayer')
parser.add_argument('--infix', '-i', default='VID-')
args = parser.parse_args()

# queue = []
event_name = ''
event_date = None


def get_date(name):
    """Naive date extractor from filename, it must already be there in big endian (e.g. ISO) format."""
    name = re.sub(r'\D', '', name)  # remove non-digits
    return name[:4] + '-' + name[4:6] + '-' + name[6:8]


def move(name, target_directory):
    print('Renaming {} into {}'.format(name, target_directory))
    if not os.path.isdir(target_directory):
        os.makedirs(target_directory)
    os.rename(name, os.path.join(target_directory, name))


for filename in sorted(itertools.chain.from_iterable(map(glob.glob, args.files))):
    while True:
        os.system(args.player + ' ' + filename)
        print('Event name (empty = {}, delete/rm/del/- = move to _trash)'.format(event_name))
        answer = sys.stdin.readline().strip()

        if answer not in ('re', 'replay', '<'):
            break

    if answer in ('delete', 'rm', 'del', '-'):
        move(filename, '_trash')
        continue

    if answer:
        event_name = answer.replace(' ', '-')
        event_date = None

    if not event_date:
        event_date = get_date(filename)

    move(filename, event_date + '-' + args.infix + event_name)
