#!/usr/bin/env python

def main(maxcols = 0):
    """Read input lines, split and pad to have even columns."""
    import re
    import sys

    def pad(s, n):
        return s + (n-len(s))*' ' if len(s) < n else s

    rows = []
    indents = []
    try:
        while True:
            line = raw_input()
            rows.append(line.split(None, maxcols-1))
            indents.append(re.match('\s+', line))
    except EOFError:
        pass
    max_cols = max(map(len, rows))
    max_lens = [0] * max_cols
    for row in rows:
        for i in xrange(len(row)):
            max_lens[i] = max(max_lens[i], len(row[i]))
    for row, indent in zip(rows, indents):
        if indent:
            sys.stdout.write(indent.group())
        for i in xrange(len(row)-1):
            print pad(row[i], max_lens[i]),
        if len(row) > 0:
            print row[-1]
        else:
            print

if __name__ == '__main__':
    import sys
    maxcols = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(maxcols)

