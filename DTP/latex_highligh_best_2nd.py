#!/usr/bin/env python

import sys


def transpose(nested):
    return [list(x) for x in zip(*nested)]


def is_float(item):
    try:
        float(item)
    except ValueError:
        return False
    return True


def highlight(col, reverse=False):
    if not all(is_float(item) for item in col):
        return col

    def markup(item, rank):
        if rank == 1:
            return '\\textbf{' + item + '}'
        if rank == 2:
            return '\\underline{' + item + '}'
        return item

    sorted_vals = sorted(set(col), key=float, reverse=not reverse)
    ranks = {val: rank + 1 for rank, val in enumerate(sorted_vals)}

    return [markup(item, ranks[item]) for item in col]


lines = [line.strip() for line in sys.stdin.readlines()]

assert all(line.endswith(r"\\") for line in lines)

rows = [[item.strip() for item in line[:-2].split("&")] for line in lines]

cols = transpose(rows)

new_rows = transpose(highlight(col) for col in cols)

for row in new_rows:
    print(" & ".join(row) + r" \\")

