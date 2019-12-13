#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import glob
import re
import subprocess

try:
    from natsort import natsorted
except ImportError:
    natsorted = sorted

# partially based on:
# https://stackoverflow.com/a/3844467/1338797

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--separator', '-s', help='Output separator for CSV', default=';')


def parse_duration(s):
    # credits: https://stackoverflow.com/a/42543326/1338797
    from datetime import datetime as dtt
    FORMAT = '%H:%M:%S'
    return dtt.strptime(s, FORMAT) - dtt.strptime('00:00:00', FORMAT)


def get_duration(filename, verbose=False):
    result = subprocess.Popen(
        ["ffprobe", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    duration = [x.decode() for x in result.stdout.readlines() if b'Duration' in x]
    if verbose:
        print(filename, duration)
    time_string = re.search(r'Duration:\s*([\d:]+)', duration[0]).group(1)
    if verbose:
        print('extracted time:', time_string)
    return time_string


if __name__ == '__main__':
    args = parser.parse_args()
    deltas = []

    for pattern in args.files:
        for name in natsorted(glob.glob(pattern)):
            duration = get_duration(name, args.verbose)
            deltas.append(parse_duration(duration))
            print('{}{}{}'.format(name, args.separator, duration))

    if len(deltas):
        total = sum(deltas, datetime.timedelta())
        print('Total{}{}'.format(args.separator, total))
