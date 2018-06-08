#!/usr/bin/env python

import sys
import mmap

WHOLE_FILE = 0


def process(filename):
    with open(filename, 'r+b') as stream:
        mapped_file = mmap.mmap(stream.fileno(), WHOLE_FILE)
        idx = mapped_file.find(b'mvhd')
        if idx == -1:
            print(filename, '- not found')
        else:
            print(filename, '- mvhd found at index:', idx)
        mapped_file.close()


if __name__ == '__main__':
    for argument in sys.argv[1:]:
        process(argument)
