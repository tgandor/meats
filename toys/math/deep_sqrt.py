#!/usr/bin/env python

"""
Do what bc(1) can do as well.
"""

import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("x", type=int)
parser.add_argument("digits", type=int)
args = parser.parse_args()

x = args.x
num = int(math.sqrt(x))
den = 1

for d in range(args.digits):
    num *= 10
    den *= 10
    dig = 9
    for i in range(9):
        num += 1
        if num**2 > x * den * den:
            num -= 1
            break
    print(f"{num} / 10**{d+1}")
