"""
Stochastic tree / binomial distribution via dynamic programming.

p[i][j] = probability of getting exactly j heads and i tails
           after i+j fair coin flips = C(i+j, j) / 2^(i+j)

Recurrence:
    p[0][0] = 1
    p[i][j] = (p[i-1][j] + p[i][j-1]) / 2   (missing terms treated as 0)
"""

import argparse
from fractions import Fraction


def main():
    parser = argparse.ArgumentParser(description="Binomial stochastic tree via DP")
    parser.add_argument("a", type=int, help="max heads (columns)")
    parser.add_argument("t", type=int, help="max tails (rows)")
    parser.add_argument("-f", "--fraction", action="store_true",
                        help="use exact Fraction arithmetic instead of float")
    args = parser.parse_args()

    zero, one = (Fraction(0), Fraction(1)) if args.fraction else (0.0, 1.0)

    p = [[zero] * (args.a + 1) for _ in range(args.t + 1)]
    p[0][0] = one

    for i in range(args.t + 1):
        for j in range(args.a + 1):
            if i == 0 and j == 0:
                continue
            above = p[i - 1][j] if i > 0 else zero
            left  = p[i][j - 1] if j > 0 else zero
            p[i][j] = (above + left) / 2

    if args.fraction:
        fmt = lambda x: f"{str(x):>12s}"
    else:
        fmt = lambda x: f"{x:8.4f}"

    for row in p:
        print(" ".join(fmt(x) for x in row))


if __name__ == "__main__":
    main()
