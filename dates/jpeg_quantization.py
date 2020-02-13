#!/usr/bin/env python

# Inspired by:
# https://codereview.stackexchange.com/questions/171370/read-quantization-tables-from-jpeg-files
# taking magics etc. from there

import glob
import mmap
import sys

DEFINE_QUANTIZATION_TABLE = b'\xff\xdb'
SINGLE_TABLE_PAYLOAD_DATA = b'\x00\x43'
DOUBLE_TABLE_PAYLOAD_DATA = b'\x00\x84'

WHOLE_FILE = 0

DEBUG = True


def display(table):
    print(table)
    try:
        import numpy as np
        print(np.array(list(table[1:]), dtype=np.uint8).reshape(8, -1))
    except ImportError:
        # cheap substitute
        import pprint
        pprint.pprint([
            list(table[row_start:row_start+8])
            for row_start in range(1, 65, 8)
        ])



def find_quantization_tables(filename):
    with open(filename, 'r+b') as stream:
        mapped_file = None
        try:
            # mmap is a context manager, but only in 3.2+
            mapped_file = mmap.mmap(stream.fileno(), WHOLE_FILE)

            # it seems the DQT needs to be at an even offset?
            idx = -1
            double = False
            while True:
                idx = mapped_file.find(DEFINE_QUANTIZATION_TABLE, idx+1)

                if idx == -1:
                    print(filename, '- DEFINE_QUANTIZATION_TABLE not found')
                    return

                if idx % 2 == 0:
                    payload_kind = mapped_file[idx+2:idx+4]


                    if payload_kind == SINGLE_TABLE_PAYLOAD_DATA:
                        print(filename, '- DEFINE_QUANTIZATION_TABLE + Single QT found at offset:', idx, 'hex:', hex(idx))
                        # break
                    elif payload_kind == DOUBLE_TABLE_PAYLOAD_DATA:
                        print(filename, '- DEFINE_QUANTIZATION_TABLE + Double QT found at offset:', idx, 'hex:', hex(idx))
                        double = True
                        # break
                    elif DEBUG:
                        print(filename, idx, ': Neither Single nor Double QT found...')

                # this might have been after break, but there can be many tables...
                # or maybe stray markers, followed by some bytes...
                tab_start = idx + 4
                tab_size = 130 if double else 65

                table = mapped_file[tab_start:tab_start + tab_size]
                if double:
                    display(table[:65])
                    display(table[65:])
                else:
                    display(table)

        finally:
            if mapped_file:
                mapped_file.close()


if __name__ == '__main__':
    for argument in sys.argv[1:]:
        for fn in glob.glob(argument):
            find_quantization_tables(fn)
