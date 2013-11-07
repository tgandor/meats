#!/usr/bin/env python

import sys

def human(x):
    for sufix in ['', 'K', 'M', 'G', 'T']:
        if x < 1024:
            return "%.2f %s" % (x, sufix) if x - int(x) > 0.001 else "%d %s" % (int(x), sufix)
        x /= 1024.0
    return "%.1f P" % x

if __name__ == '__main__':
	print human(int(sys.argv[1]))

