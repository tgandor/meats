#!/usr/bin/env python

import sys


def transpose(nested):
    return [list(x) for x in zip(*nested)]


def _parse(item):
    if "," in item:
        thousand_comma = item.count(",") > 1 or "." in item
        item = item.replace(",", "" if thousand_comma else ".")
    return float(item.replace(" ", ""))


def is_float(item):
    try:
        _parse(item)
    except ValueError:
        return False
    return True


def highlight(col, reverse=False):
    if not all(is_float(item) for item in col):
        return col

    def markup(item, rank):
        if rank == 1:
            return "\\textbf{" + item + "}"
        if rank == 2:
            return "\\underline{" + item + "}"
        return item

    sorted_vals = sorted(set(col), key=_parse, reverse=not reverse)
    ranks = {val: rank + 1 for rank, val in enumerate(sorted_vals)}

    return [markup(item, ranks[item]) for item in col]


lines = [line.strip() for line in sys.stdin.readlines()]

assert all(line.endswith(r"\\") for line in lines)

rows = [[item.strip() for item in line[:-2].split("&")] for line in lines]

cols = transpose(rows)

negatives = set(int(x) if int(x) >= 0 else len(cols) + int(x) for x in sys.argv[1:])

new_rows = transpose(
    highlight(col, reverse=i in negatives) for i, col in enumerate(cols)
)

for row in new_rows:
    print(" & ".join(row) + r" \\")
