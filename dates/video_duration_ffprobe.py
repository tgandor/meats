from __future__ import print_function

import argparse
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


def get_duration(filename, verbose=False):
    result = subprocess.Popen(
        ["ffprobe", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    duration = [x.decode() for x in result.stdout.readlines() if b'Duration' in x]
    if verbose:
        print(filename, duration)
    time_string = re.search('Duration:\s*([\d:]+)', duration[0]).group(1)
    if verbose:
        print('extracted time:', time_string)
    return time_string


if __name__ == '__main__':
    args = parser.parse_args()
    for pattern in args.files:
        for name in natsorted(glob.glob(pattern)):
            duration = get_duration(name, args.verbose)
            print('{}{}{}'.format(name, args.separator, duration))
