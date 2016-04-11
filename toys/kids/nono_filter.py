#!/usr/bin/env python

import sys

MARKED = '#'
EXCLUDED = 'X'
EMPTY = '.'


def main():
    if len(sys.argv) < 2:
        print('Usage: nono_filter.py <+MARKED|-EXCLUDED|EMPTY>...')
        exit()
    chunks = []
    for arg in sys.argv[1:]:
        if arg.startswith('+'):
            chunks.append(MARKED * int(arg[1:]))
        elif arg.startswith('-'):
            chunks.append(EXCLUDED * int(arg[1:]))
        else:
            chunks.append(EMPTY * int(arg))
    print(''.join(chunks))


if __name__ == '__main__':
    main()
