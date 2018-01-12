#!/usr/bin/env python

from __future__ import print_function

import os
import glob
from itertools import chain
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--stabilize', '-stab', action='store_true')
parser.add_argument('--copy-audio', '-c', action='store_true')
parser.add_argument('--quality', '-q', type=int, default=24)
parser.add_argument('files_or_globs', type=str, nargs='+')


def time_format(duration):
    """Format a float of seconds as number and H:M:S string.

    For example:
    >>> time_format(123)
    '123.00 s (00:02:03)'

    >>> time_format(12345.67)
    '12345.67 s (03:25:45)'
    """
    duration_tuple = time.gmtime(duration)
    return '{:.2f} s ({})'.format(float(duration), time.strftime('%H:%M:%S', duration_tuple))


class TimedSystem:
    def __init__(self):
        self.total = 0
        self.log = []

    def run(self, command):
        start = time.time()
        print(time.strftime('%H:%M:%S'), 'starting', command)
        os.system(command)
        finish = time.time()
        elapsed = finish - start
        print(time.strftime('%H:%M:%S'), 'finished in: ', time_format(elapsed))
        self.total += elapsed
        self.log.append((command, start, finish, elapsed))


try:
    from shutil import which
except ImportError:
    def which(program):
        # https://stackoverflow.com/a/377028/1338797
        import os

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None


if __name__ == '__main__':
    args = parser.parse_args()

    options = '-map_metadata 0 -pix_fmt yuv420p -crf {} -preset veryslow -strict -2'.format(
        args.quality
    )

    os.makedirs('original', exist_ok=True)
    os.makedirs('converted', exist_ok=True)

    converter = which('ffmpeg')
    if converter is None:
        converter = which('avconv')
    if converter is None:
        print('Neither ffmpeg nor avconv found.')
        exit()

    print('Using:', converter)

    ts = TimedSystem()

    for filename in chain.from_iterable(map(glob.glob, args.files_or_globs)):
        basename = os.path.basename(filename)
        original = os.path.join('original', basename)
        os.rename(filename, original)
        converted = os.path.splitext(os.path.join('converted', basename))[0] + '.mp4'
        filters = ''
        if args.stabilize:
            preprocessing = '{} -i "{}" -vf vidstabdetect -f null -'.format(
                converter,
                original
            )
            ts.run(preprocessing)
            filters += ' -vf vidstabtransform,unsharp=5:5:0.8:3:3:0.4'

        commandline = '{} -i "{}" {} -c:a {} -c:v h264 {} "{}"'.format(
            converter,
            original,
            filters,
            'copy' if args.copy_audio else 'aac',
            options,
            converted)
        ts.run(commandline)

    print('Finished in: ', time_format(ts.total))
