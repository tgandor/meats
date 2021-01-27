#!/usr/bin/env python
from __future__ import print_function

# print collatz sequence starting from some number

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('n', type=int)
parser.add_argument('--newline', '-n', action='store_true')
parser.add_argument('--quiet', '-q', action='store_true')
args = parser.parse_args()

n = args.n
m = 0
iterations = 0
print(n, end='\n' if args.newline else ' ')

while True:
    if n % 2 == 0:
        n //= 2
    else:
        n = 3 * n + 1

    iterations += 1
    m = max(n, m)
    print(n, end='\n' if args.newline else ' ')
    if n == 1:
        break

if not args.quiet:
    print('- after', iterations, 'iterations.', 'Max =', m)
