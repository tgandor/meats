#!/usr/bin/env python

import argparse
import re
import time

parser = argparse.ArgumentParser()
parser.add_argument('size')
parser.add_argument('speed_per_second')
args = parser.parse_args()

FACTORS = {
    suffix: 1024**(i+1)
    for i, suffix in enumerate('KMGTP')
}
FACTORS[None] = 1


def parse_human(size):
    """Return number of bytes in

    >>> parse_human('12')
    12
    >>> parse_human('1k')
    1024
    """

    m = re.match(r'(\d+)(\.\d*)?([kmgtp]?)$', size, re.IGNORECASE)
    assert m, r'size must match (\d+)(\.\d*)?([kmgtp]?)$'
    print(m, m.groups())
    whole, frac, unit = m.groups()

    result = int(whole)
    if frac:
        result += float(frac)
    if unit:
        result *= FACTORS[unit]

    return result


num_bytes = parse_human(args.size)
bauds = parse_human(args.speed_per_second)
