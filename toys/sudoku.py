#!/usr/bin/env python

import argparse
import copy
from itertools import combinations, chain

import pycosat

# variable encoding: (row, col, val) = 81 * row + 9 * col + val


def var_to_val(var):
    var -= 1
    return var // 81, var // 9 % 9, var % 9


def val_to_var(row, col, val):
    # return row, col, val
    return 81 * row + 9 * col + val + 1


def test_assignment():
    for var in range(9 * 9 * 9):
        row, col, val = var_to_val(var)
        var2 = val_to_var(row, col, val)
        assert var == var2


def chunks(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


# SAT helpers


def one_and_only_one(values):
    yield values
    # return
    for a, b in combinations(values, 2):
        yield [-a, -b]


def one_digit_per_field():
    for row in range(9):
        for col in range(9):
            yield from one_and_only_one([val_to_var(row, col, val) for val in range(9)])


def one_digit_per_row():
    for col in range(9):
        for val in range(9):
            yield from one_and_only_one([val_to_var(row, col, val) for row in range(9)])


def one_digit_per_col():
    for row in range(9):
        for val in range(9):
            yield from one_and_only_one([val_to_var(row, col, val) for col in range(9)])


def square(sx, sy):
    for row in range(3 * sx, 3 * sx + 3):
        for col in range(3 * sy, 3 * sy + 3):
            yield row, col


def one_digit_per_square():
    for sx in range(3):
        for sy in range(3):
            for val in range(9):
                yield from one_and_only_one(
                    [val_to_var(row, col, val) for row, col in square(sx, sy)]
                )


base_sudoku = list(
    chain(
        one_digit_per_field(),
        one_digit_per_row(),
        one_digit_per_col(),
        one_digit_per_square(),
    )
)

parser = argparse.ArgumentParser()
parser.add_argument("unsolved", help=".txt file, no spaces, 0=empty")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()


for data in chunks(map(str.strip, open(args.unsolved)), 9):
    sudoku = base_sudoku[:]
    for row, values in enumerate(data):
        for col, value in enumerate(map(int, values)):
            if value:
                sudoku.append([val_to_var(row, col, value - 1)])
    data = list(map(list, data))
    if args.verbose:
        for line in data:
            print(" ".join(line))

    orig = data
    found = 0

    for solution in pycosat.itersolve(sudoku):
        found += 1
        marked = [s for s in solution if s > 0]
        data = copy.deepcopy(orig)
        if args.verbose:
            print(len(marked), marked)
        print("-" * 40)
        for var in marked:
            row, col, value = var_to_val(var)
            data[row][col] = str(value + 1)
        for line in data:
            print(" ".join(line))

    if found > 1:
        print(f"Bad sudoku, {found} solutions found.")

    print("=" * 40)
