import sys
from itertools import combinations
import pycosat
import argparse

board_size = 8


def field(r, c):
    """Variable index for field (r, c)."""
    return board_size * (r-1) + c


def _no_two_at_once(values):
    for a, b in combinations(values, 2):
        yield [-a, -b]


def _one_and_only(values):
    yield values
    yield from _no_two_at_once(values)


def row(r):
    yield from _one_and_only([field(r, c) for c in range(1, board_size+1)])


def col(c):
    yield from _one_and_only([field(r, c) for r in range(1, board_size+1)])


def slash(r, c):
    a = []
    while r <= board_size and c <= board_size:
        a.append(field(r, c))
        r += 1
        c += 1
    yield from _no_two_at_once(a)


def backslash(r, c):
    a = []
    while r <= board_size and c > 0:
        a.append(field(r, c))
        r += 1
        c -= 1
    yield from _no_two_at_once(a)


def output(sol):
    # print(sol)
    for i in range(board_size):
        print(''.join('.' if sol[board_size*i + j] < 0 else 'Q' for j in range(board_size)))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', '-n', type=int, choices=range(3, 21), default=8)
    parser.add_argument('--all', '-a', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    global board_size
    board_size = args.size

    clauses = []
    for i in range(1, args.size+1):
        clauses.extend(row(i))
        clauses.extend(col(i))
    for r in range(1, args.size):
        clauses.extend(slash(r, 1))
        clauses.extend(backslash(r, args.size))
    for c in range(2, args.size):
        clauses.extend(slash(1, c))
        clauses.extend(backslash(1, c))
    # print(clauses)

    if not args.all:
        sol = pycosat.solve(clauses)
        if sol == 'UNSAT':
            print('Bad luck - no solution')
            exit()
        output(sol)
    else:
        for i, sol in enumerate(pycosat.itersolve(clauses)):
            print(i+1)
            output(sol)
            print('=' * 10)


if __name__ == '__main__':
    main()

