#!/usr/bin/env python

import binascii
import sys
import re


def get_streams():
    in_ = sys.stdin
    out_ = sys.stdout
    args = sys.argv[1:]
    if '-o' in args:
        idx = args.index('-o')
        args.pop(idx)
        if idx >= len(args):
            sys.stderr.write('{}: no argument specified for `-o` option\n'.format(sys.argv[0]))
            exit(1)
        out_ = open(args[idx], 'wb')
        args.pop(idx)
    if len(args) > 0:
        in_ = open(args[0])
    return in_, out_


in_, out_ = get_streams()
prefix = in_.read(2)
if prefix.lower() != '0x':
    out_.write(binascii.unhexlify(prefix))

non_hex = re.compile('[^a-fA-F0-9]+')

while True:
    chunk = in_.read(2**12)
    if not chunk:
        break
    chunk = non_hex.sub('', chunk)
    try:
        out_.write(binascii.unhexlify(chunk))
    except TypeError:
        sys.stderr.write('Error in chunk: {}\n'.format(repr(chunk)))
        break

