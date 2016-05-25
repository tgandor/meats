#!/usr/bin/env python

import sys
import time

def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

if __name__=='__main__':
    start = time.time()
    n = int(sys.argv[1]) if len(sys.argv) >= 2 else 34
    fib_n = fib(n)
    elapsed = time.time() - start
    calls = 2*fib_n-1
    print("fib({}) = {}; {:.3f} s elapsed. {:,} calls, {:,.0f} c/s.".format(
        n, fib_n, elapsed, calls, calls/elapsed
    ))
