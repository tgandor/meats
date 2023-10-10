#!/usr/bin/env python

import sys


def gen_ranges(path):
    s = t = None
    with open(path) as f:
        for line in f:
            try:
                n = int(line)
                if s is None:
                    s = n
                    continue
                if t is None:
                    if n == s+1:
                        t = n
                        continue
                    else:
                        yield s
                        s = n
                        continue
                if n != t + 1:
                    yield (s, t)
                    s, t = n, None
                    continue
                t = n
            except ValueError:
                if t is not None:
                    yield (s, t)
                elif s is not None:
                    yield s
                yield line.rstrip()
                s = t = None
        if t is not None:
            yield (s, t)
        elif s is not None:
            yield s


for x in gen_ranges(sys.argv[1]):
    print(x)
