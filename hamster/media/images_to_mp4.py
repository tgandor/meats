#!/usr/bin/env python

# inspired by:
# https://stackoverflow.com/a/37478183/1338797

from __future__ import print_function
from __future__ import division

import argparse
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument('--bitrate', '-b', help='specify output bitrate for video')
parser.add_argument('--converter', help='manually specify [full path to] ffmpeg or avconv')
parser.add_argument('--deinterlace', '-d', action='store_true', help='deinterlace with yadif')
parser.add_argument('--duration', '-t', help='duration limit for encoding')
parser.add_argument('--framerate', '-r', help='specify input and output FPS for video', default=25)
parser.add_argument('--nvenc', '-nv', action='store_true')
parser.add_argument('--output', '-o', help='output file', default='images.mp4')
parser.add_argument('--quality', '-q', default=22)
parser.add_argument('--stabilize', '-stab', action='store_true')
parser.add_argument('--start', '-ss', help='start time for encoding in seconds')
parser.add_argument('files_glob', help='glob expression (not expanded) for input files')


def duration_format(duration):
    """Format a float of seconds as number and H:M:S string.

    For example:
    >>> duration_format(123)
    '123.00 s (00:02:03)'

    >>> duration_format(12345.67)
    '12345.67 s (03:25:45)'
    """
    duration_tuple = time.gmtime(duration)
    return '{:.2f} s ({})'.format(float(duration), time.strftime('%H:%M:%S', duration_tuple))


def time_format(timestamp):
    time_tuple = time.gmtime(timestamp)
    return time.strftime('%H:%M:%S', time_tuple)


class TimedSystem:
    def __init__(self):
        self.total = 0
        self.log = []

    def run(self, command):
        start = time.time()
        print(time.strftime('%H:%M:%S'), 'starting', command)
        status = os.system(command)
        finish = time.time()
        elapsed = finish - start
        print(time.strftime('%H:%M:%S'), 'finished in: ', duration_format(elapsed))
        self.total += elapsed
        self.log.append((command, start, finish, elapsed))
        if status != 0:
            raise RuntimeError('Error (status={}) executing command: {}'.format(status, command))
        return status

    def report(self):
        for command, start, finish, elapsed in self.log:
            print(time_format(start), command)
            print(time_format(finish), 'took:', duration_format(elapsed))
        print(time.strftime('%H:%M:%S'), 'Finished in: ', duration_format(self.total))


def ratio_format(pre, post):
    return '{:,}\t{:,}\t{:.1f}%\t{:.1f}x\t{:,}'.format(pre, post, 100*post/pre, pre/post, post-pre)


try:
    from shutil import which
except ImportError:
    def which(program):
        # https://stackoverflow.com/a/377028/1338797
        import os

        def is_exe(file_path):
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

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

    input_options = '-framerate {} -pattern_type glob'.format(args.framerate)

    common_options = '-pix_fmt yuv420p'

    if args.deinterlace:
        common_options += ' -vf yadif'

    if args.nvenc:
        encoder_options = 'h264_nvenc -cq {} -preset slow {}'.format(args.quality, common_options)
    else:
        encoder_options = 'h264 -crf {} -preset veryslow {}'.format(args.quality, common_options)

    if args.bitrate:
        encoder_options += ' -b:v {}'.format(args.bitrate)

    if args.framerate:
        encoder_options += ' -r {}'.format(args.framerate)

    converter = args.converter
    if converter is None:
        converter = which('ffmpeg')
    if converter is None:
        converter = which('avconv')
    if converter is None:
        print('Neither ffmpeg nor avconv found.')
        exit()

    print('Using:', converter)

    ts = TimedSystem()

    original = args.files_glob
    converted = args.output

    filters = ''
    if args.stabilize:
        preprocessing = '{} {} -i "{}" -vf vidstabdetect -f null -'.format(
            converter,
            input_options,
            original
        )
        ts.run(preprocessing)
        filters += ' -vf vidstabtransform,unsharp=5:5:0.8:3:3:0.4'

    if args.start:
        filters += ' -ss {:.2f}'.format(args.start)

    commandline = '{} {} -i "{}" {} -c:v {} "{}"'.format(
        converter,
        input_options,
        original,
        filters,
        encoder_options,
        converted)
    ts.run(commandline)
    ts.report()
