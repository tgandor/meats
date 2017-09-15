#!/usr/bin/env python

import os
import sys
import glob
from itertools import chain

try:
    from shutil import  which
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

options = '-map_metadata 0 -pix_fmt yuv420p -crf 26 -preset veryslow -strict -2'

os.makedirs('original', exist_ok=True)
os.makedirs('converted', exist_ok=True)

converter = which('ffmpeg')
if converter is None:
    converter = which('avconv')
if converter is None:
    print('Neither ffmpeg nor avconv found.')
    exit()

print('Using:', converter)

for filename in chain.from_iterable(map(glob.glob, sys.argv[1:])):
    basename = os.path.basename(filename)
    original = os.path.join('original', basename)
    os.rename(filename, original)
    converted = os.path.splitext(os.path.join('converted', basename))[0] + '.mp4'
    os.system('{} -i "{}" -c:a aac -c:v h264 {} "{}"'.format(
        converter,
        original,
        options,
        converted
    ))
