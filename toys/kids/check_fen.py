#!/usr/bin/env python

from __future__ import print_function

import sys
import re


def line_stats(line):
    res = {}
    len_ = 0
    for c in line:
        if '0' <= c <= '8':
            len_ += int(c)
        elif c.lower() in 'kqrbnp':
            len_ += 1
            res[c] = res.get(c, 0) + 1
        else:
            print('Illegal character', c, 'in line', line)
    if len_ != 8:
        print('Line', line, 'has', len_, 'squares')
    else:
        print('Line', line, 'ok')
    return res


def check_position(fen):
    lines = fen.split('/')
    if len(lines) != 8:
        print('Wrong number of lines', len(lines))

    partials = []
    total = {}
    for line in lines:
        partial = line_stats(line)
        for k in partial:
            total[k] = total.get(k, 0) + partial[k]
        partials.append(partial)

    white_king = total.get('K', 0)
    if white_king != 1:
        print('Position has', white_king, 'white kings')

    black_king = total.get('k', 0)
    if black_king != 1:
        print('Position has', black_king, 'black kings')

    for pawn in 'pP':
        if pawn in total and total[pawn] > 8:
            print('There are', total[pawn], pawn, 'pawns')

    for i in (0, 7):
        if 'p' in partials[i] or 'P' in partials[i]:
            print('Pawns on line', i+1)

    print('Piece counts:', total)

for line in sys.stdin:
    parts = line.split()
    print(parts)
    check_position(parts[0])
