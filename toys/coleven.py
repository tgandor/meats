#!/usr/bin/env python

def main():
    """Read input lines, split and pad to have even columns."""

    def pad(s, n):
        return s + (n-len(s))*' ' if len(s) < n else s

    rows = []
    try:
        while True:
            rows.append(raw_input().split())
    except EOFError:
        pass
    max_cols = max(map(len, rows))
    max_lens = [0] * max_cols
    for row in rows:
        for i in xrange(len(row)):
            max_lens[i] = max(max_lens[i], len(row[i]))
    for row in rows:
        for i in xrange(len(row)):
            print pad(row[i], max_lens[i]),
        print

if __name__ == '__main__':
    main()

