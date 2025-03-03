#!/usr/bin/env python

"""
Do what bc(1) can do as well.
"""

import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("x", type=int)
parser.add_argument("digits", type=int, nargs="?", default=21)
parser.add_argument(
    "--order", "-o", type=int, default=2, help="root order, i.e. 3, for cube"
)
args = parser.parse_args()

x = args.x
n = args.order
num = int(x ** (1 / n))
den = 1

for d in range(args.digits):
    num *= 10
    den *= 10
    for i in range(9):
        num += 1
        if num**n > x * den**n:
            num -= 1
            break
    print(f"{num} / 10**{d+1}")

print(f"Float result: {x ** (1 / n):.{args.digits}f}")
