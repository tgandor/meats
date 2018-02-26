import sys
from itertools import combinations
import pycosat


def field(r, c):
    """Variable index for field (r, c)."""
    return 8*(r-1) + c


def _no_two_at_once(values):
    for a, b in combinations(values, 2):
        yield [-a, -b]


def _one_and_only(values):
    yield values
    yield from _no_two_at_once(values)


def row(r):
    yield from _one_and_only([field(r, c) for c in range(1, 9)])


def col(c):
    yield from _one_and_only([field(r, c) for r in range(1, 9)])


def slash(r, c):
    a = []
    while r < 9 and c < 9:
        a.append(field(r, c))
        r += 1
        c += 1
    yield from _no_two_at_once(a)


def backslash(r, c):
    a = []
    while r < 9 and c > 0:
        a.append(field(r, c))
        r += 1
        c -= 1
    yield from _no_two_at_once(a)


def output(sol):
    # print(sol)
    for i in range(8):
        print(''.join('.' if sol[8*i + j] < 0 else 'Q' for j in range(8)))


def main():
    clauses = []
    for i in range(1, 9):
        clauses.extend(row(i))
        clauses.extend(col(i))
    for r in range(1, 8):
        clauses.extend(slash(r, 1))
        clauses.extend(backslash(r, 8))
    for c in range(2, 8):
        clauses.extend(slash(1, c))
        clauses.extend(backslash(1, c))
    # print(clauses)

    if len(sys.argv) < 2:
        sol = pycosat.solve(clauses)
        if sol == 'UNSAT':
            print('Bad luck - no solution')
            exit()
        output(sol)
    else:
        for sol in pycosat.itersolve(clauses):
            output(sol)
            print('=' * 10)


if __name__ == '__main__':
    main()

