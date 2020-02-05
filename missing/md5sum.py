#!/usr/bin/env python

from zlib import crc32

import argparse
import glob
import hashlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--sha256', '-S', action='store_true', help='Use SHA256 instead of MD5')
parser.add_argument('--sha', '-s', action='store_true', help='Use SHA-1 instead of MD5')
parser.add_argument('--crc', '-c', action='store_true', help='Use CRC32 instead of MD5')
parser.add_argument('files', nargs='*')
args = parser.parse_args()

# inspired by:
# http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file


class Crc32:
    def __init__(self):
        self.value = 0

    def update(self, data):
        # see about signedness:
        # https://stackoverflow.com/questions/30092226/how-to-calculate-crc32-with-python-to-match-online-results
        self.value = crc32(data, self.value) & 0xffffffff

    def hexdigest(self):
        # return hex(self.value).upper()[2:]
        return '{:08X}'.format(self.value)


def do_md5(file_obj):
    if args.sha256:
        hasher = hashlib.sha256()
    elif args.sha:
        hasher = hashlib.sha1()
    elif args.crc:
        # in memory CRC - may fail for large streams:
        # return hex(crc32(file_obj.read()) & 0xffffffff).upper()[2:]
        hasher = Crc32()
    else:
        hasher = hashlib.md5()

    for chunk in iter(lambda: file_obj.read(2**22), b""):
        hasher.update(chunk)
    return hasher.hexdigest()


def md5(filename):
    if filename == '-':
        digest = do_md5(sys.stdin)
    else:
        with open(filename, "rb") as f:
            digest = do_md5(f)
    print('{}  {}'.format(digest, filename))


def _main():
    if len(args.files) < 1:
        md5('-')
    else:
        for expr in args.files:
            if '*' in expr:
                for filename in glob.glob(expr):
                    md5(filename)
            else:
                md5(expr)


if __name__ == '__main__':
    _main()
