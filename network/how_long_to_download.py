#!/usr/bin/env python

import argparse
import datetime
import re
import time

FACTORS = {
    suffix: 1024**(i+1)
    for i, suffix in enumerate('KMGTP')
}
# no generator possible: dict size changed during iteration
FACTORS.update([(k.lower(), v) for k, v in FACTORS.items()])
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
    # print(m, m.groups())
    whole, frac, unit = m.groups()

    result = int(whole)
    if frac:
        result += float(frac)
    if unit:
        result *= FACTORS[unit]

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('size')
    parser.add_argument('speed_per_second')
    args = parser.parse_args()

    num_bytes = parse_human(args.size)
    bauds = parse_human(args.speed_per_second)

    seconds = num_bytes / bauds
    print('ETA: {:.1f} seconds:\n=    {}'.format(seconds, datetime.timedelta(seconds=seconds)))
    print('ETD: {}'.format(datetime.datetime.now() + datetime.timedelta(seconds=seconds)))
