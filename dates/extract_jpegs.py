#!/usr/bin/env python

from __future__ import print_function

import argparse
import glob
import mmap
import os

WHOLE_FILE = 0


def get_size(buffer, idx):
    s1 = buffer[idx + 2]
    s2 = buffer[idx + 3]
    return s1 * 256 + s2


def save_jpeg(orig_filename, jpeg_number, data):
    basename, _ = os.path.splitext(orig_filename)
    target = '{}_jpg_{:04d}.jpg'.format(basename, jpeg_number)
    with open(target, 'wb') as out_file:
        out_file.write(data)


def extract_jpegs(filename):
    with open(filename, 'r+b') as stream:
        mapped_file = mmap.mmap(stream.fileno(), WHOLE_FILE)
        idx = -1
        jpeg_number = 0
        jpeg_begin = None

        while True:
            idx = mapped_file.find(b'\xff', idx + 1)
            if idx == -1:
                print('No more FFs')
                break

            marker = mapped_file[idx+1]
            # https://stackoverflow.com/questions/4585527/detect-eof-for-jpg-images
            if 0xd0 <= marker <= 0xd9 or marker <= 1:
                if marker == 0xd8:
                    print('SOI (FFD8) at:', idx)
                    jpeg_number += 1
                    jpeg_begin = idx
                elif marker == 0xd9:
                    print('EOI (FFD9) at:', idx)
                    if jpeg_begin is None:
                        print('!!! EOI without SOI')
                        continue
                    save_jpeg(filename, jpeg_number, mapped_file[jpeg_begin:idx+2])
                    print('Saved jpeg #', jpeg_number)
                    jpeg_begin = None
                elif marker:
                    print('Magic marker', marker, 'at:', idx)
                idx += 1
                continue

            if args.verbose:
                print('Found FF', hex(marker), 'at', idx)

            size = get_size(mapped_file, idx)
            if args.verbose:
                print('- having size:', size)

            if marker == 0xe0:
                segment_type = str(mapped_file[idx+4:idx+8])
                print('- which is', segment_type, 'at', idx, 'size', size)
            idx += size + 1

        mapped_file.close()


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+')
parser.add_argument('--verbose', '-v', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()
    for pattern in args.files:
        for name in glob.glob(pattern):
            extract_jpegs(name)
