#!/usr/bin/env python

import hashlib
import sys


# inspired by:
# http://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file


def do_md5(fileobj):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: fileobj.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5(fname):
    if fname == '-':
        digest = do_md5(sys.stdin)
    else:
        with open(fname, "rb") as f:
            digest = do_md5(f)
    print('{}  {}'.format(digest, fname))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        md5('-')
    else:
        list(map(md5, sys.argv[1:]))

