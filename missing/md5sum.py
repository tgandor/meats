#!/usr/bin/env python

import argparse
import hashlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--sha256', '-S', action='store_true', help='Use SHA256 instead of MD5')
parser.add_argument('--sha', '-s', action='store_true', help='Use SHA-1 instead of MD5')
parser.add_argument('files', nargs='*')
args = parser.parse_args()

# inspired by:
# http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file


def do_md5(file_obj):
    if args.sha256:
        hasher = hashlib.sha256()
    elif args.sha:
        hasher = hashlib.sha1()
    else:
        hasher = hashlib.md5()
    for chunk in iter(lambda: file_obj.read(4096), b""):
        hasher.update(chunk)
    return hasher.hexdigest()


def md5(filename):
    if filename == '-':
        digest = do_md5(sys.stdin)
    else:
        with open(filename, "rb") as f:
            digest = do_md5(f)
    print('{}  {}'.format(digest, filename))


if __name__ == '__main__':
    if len(args.files) < 1:
        md5('-')
    else:
        list(map(md5, args.files))
