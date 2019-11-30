# https://www.youtube.com/watch?v=_W7Yy0CNDws
# 4 Distinct Digits | hard problem from Topcoder Open 2019

from __future__ import print_function

# brute force

def find_4digit(x, l, v=False):
    start = 10 ** (l-1)
    start += x - (start % x)
    tries = 1
    while True:
        s = str(start)
        n = len(set(s))

        if v:
            print(tries, s, n)

        if len(s) != l:
            return None, tries

        if n <= 4:
            return start, tries

        start += x
        tries += 1


def clever(x, l, v=False):
    import random

    candidates = {}

    result = None
    tries = 1

    for _ in range(10 ** 6): # max tries
        like_bin = int('1' + ''.join('0' if random.random() < 0.5 else '1' for _ in range(l-1)))
        m = like_bin % x

        if v:
            print(tries, like_bin, m)

        # here was a bug!:
        # if m in candidates: ...
        # but for small L there could be a collision!

        other = candidates.get(m)
        if other and other != like_bin:
            result = abs(like_bin - other)

            padding = l - len(str(result))

            result *= 10 ** padding

            return result, tries

        tries += 1

        if other == like_bin:
            continue

        candidates[m] = like_bin

    return result, tries


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('X', type=int, nargs='?', default=9876543210)
parser.add_argument('L', type=int, nargs='?', default=120)
parser.add_argument('-v', action='store_true')
parser.add_argument('--smart', action='store_true')
args = parser.parse_args()

if args.smart:
    result, tries = clever(args.X, args.L, args.v)
else:
    result, tries = find_4digit(args.X, args.L, args.v)

# for:
# X = 28951
# L = 6
# the intelligent way seem not so intelligent after all...

print('after', tries, 'tries')
print(result)
print('mod x:', result % args.X)
