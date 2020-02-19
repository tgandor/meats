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


def zigzag(n):
    """Produce zig-zag coordinates (i, j) for (n x n) table."""
    nzigs = 2 * n - 1
    for zig in range(nzigs):
        if zig % 2 == 0:
            # odd (zigs): up (-1), right (1)
            di, dj = -1, 1
            i = min(zig, n-1)
            j = zig - i
        else:
            # even (zags): down (1), left (-1)
            di, dj = 1, -1
            j = min(zig, n-1)
            i = zig - j

        # length: zig + 1 - growing, nzigs - zig - shrinking
        len_zig = min(zig + 1, nzigs - zig)

        # print('zig', zig)
        for _ in range(len_zig):
            yield i, j
            i, j = i + di, j + dj


#for i, j in zigzag(3): print(i, j)
#exit()


def reorder(src, dest):
    gen = zigzag(8)

    for i in range(8):
        for j in range(8):
            # tricky, zigzag coordinates are destination, not source
            ti, tj = next(gen)
            dest[ti][tj] = src[i][j]


def display(table):
    print(table)
    try:
        import numpy as np
        reshaped = np.array(list(table[1:]), dtype=np.uint8).reshape(8, -1)
        reordered = np.empty_like(reshaped)
        reorder(reshaped, reordered)
        print(reordered)
    except ImportError:
        # cheap substitute
        import pprint
        import copy
        reshaped = [
            list(table[row_start:row_start+8])
            for row_start in range(1, 65, 8)
        ]
        reordered = copy.deepcopy(reshaped)
        reorder(reshaped, reordered)
        pprint.pprint(reordered)


def find_quantization_tables(filename):
    with open(filename, 'r+b') as stream:
        mapped_file = None
        try:
            # mmap is a context manager, but only in 3.2+
            mapped_file = mmap.mmap(stream.fileno(), WHOLE_FILE)

            # it seems the DQT needs to be at an even offset?
            idx = -1
            found_any = False

            while True:
                idx = mapped_file.find(DEFINE_QUANTIZATION_TABLE, idx+1)

                if idx == -1:
                    if not found_any:
                        print(filename, '- DEFINE_QUANTIZATION_TABLE not found')
                    return

                payload_kind = mapped_file[idx+2:idx+4]

                if payload_kind == SINGLE_TABLE_PAYLOAD_DATA:
                    print(filename, '- DEFINE_QUANTIZATION_TABLE + Single QT found at offset:', idx, 'hex:', hex(idx))
                    double = False
                elif payload_kind == DOUBLE_TABLE_PAYLOAD_DATA:
                    print(filename, '- DEFINE_QUANTIZATION_TABLE + Double QT found at offset:', idx, 'hex:', hex(idx))
                    double = True
                elif DEBUG:
                    # print(filename, idx, ': Neither Single nor Double QT found...')
                    continue
                else:
                    continue

                # this might have been after break, but there can be many tables...
                # or maybe stray markers, followed by some bytes...
                found_any = True
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
            print('-' * 60)
