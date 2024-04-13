#!/usr/bin/env python

import argparse
import itertools as it

import pycosat

# is black, . is light

DATA = """
#....
...#.
.....
.....
....#
"""


def to_board(text):
    board = [list(line) for line in text.strip().split("\n")]
    if len(set(len(x) for x in board)) > 1:
        raise ValueError(f"Non-uniform rows in:\n{text}")
    return board


def make_vars(board):
    n = 0
    out_vars = []
    reverse = {}
    for y, row in enumerate(board):
        out_row = []
        for x, _ in enumerate(row):
            n += 1
            out_row.append(n)
            reverse[n] = (y, x)
        out_vars.append(out_row)
    return out_vars, reverse


def nbhood(b, x, y, W, H):
    # BTW, direct translation of nbhood in PL actually means 'deleted nbhood'
    res = [b[y][x]]
    for dx in (-1, 1):
        nx = x + dx
        if 0 <= nx < W:
            res.append(b[y][nx])
    for dy in (-1, 1):
        ny = y + dy
        if 0 <= ny < H:
            res.append(b[ny][x])

    return res


def clauses_for_subsets(variables, even=False):
    """Generate CNF clauses for an odd or even 'selected' number of variables."""
    res = []
    N = len(variables)
    if not even:
        res.append(variables)
    for k in range(1 if even else 2, N + 1, 2):
        for sel in it.combinations(range(N), k):
            clause = list(variables)
            for idx in sel:
                clause[idx] *= -1
            res.append(clause)
    return res


def present(source, clicks, lookup):
    b = to_board(source)
    for c in clicks:
        y, x = lookup[c]
        b[y][x] = "X"
    print("\n".join("".join(row) for row in b))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?")
    parser.add_argument("target", nargs="?")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    if args.source:
        initial = open(args.source).read()
    else:
        parser.print_usage()
        print("(Using example data)")
        initial = DATA

    if args.verbose:
        print("Initial:")
        print(initial)

    if args.target:
        final = open(args.source).read()
    else:
        final = initial.replace("#", ".")

    if args.verbose:
        print("Final:")
        print(final)

    b1 = to_board(initial)
    b2 = to_board(final)
    if len(b1) != len(b2):
        raise ValueError(
            f"Row count mismatch between initial and final ({len(b1)} != {len(b2)})."
        )
    if len(b1[0]) != len(b2[0]):
        raise ValueError(
            f"Column count mismatch between initial and final ({len(b1[0])} != {len(b2[0])})."
        )
    H, W = len(b1), len(b1[0])

    b, lookup = make_vars(b1)
    cnf = []
    for x in range(W):
        for y in range(H):
            cnf.extend(clauses_for_subsets(nbhood(b, x, y, W, H), b1[y][x] == b2[y][x]))
    if args.verbose:
        print("#clauses and #terms total:", len(cnf), sum(len(c) for c in cnf))

    shortest = []
    len_min = H * W
    idx = 0
    for sol in pycosat.itersolve(cnf):
        idx += 1
        clicks = [x for x in sol if x > 0]
        lc = len(clicks)
        if lc < len_min:
            len_min = lc
            shortest = [clicks]
        elif lc == len_min:
            shortest.append(clicks)
        if args.verbose:
            print("Solution", idx, clicks, len(clicks), "clicks")
            present(initial, clicks, lookup)

    print(f"{len(shortest)} shortest ({len_min} clicks) solution(s)")
    if not args.verbose:
        for clicks in shortest:
            print(clicks)
            present(initial, clicks, lookup)


if __name__ == "__main__":
    main()
