#!/usr/bin/env python

# http://code.activestate.com/recipes/117119/

from __future__ import print_function
from itertools import islice


def eppstein():
    '''Yields the sequence of prime numbers via the Sieve of Eratosthenes.'''
    D = {}  # map composite integers to primes witnessing their compositeness
    q = 2   # first integer to test for primality
    while 1:
        if q not in D:
            yield q        # not marked composite, must be prime
            D[q*q] = [q]   # first multiple of q not already marked
        else:
            for p in D[q]: # move each witness to its next multiple
                D.setdefault(p+q,[]).append(p)
            del D[q]       # no longer need D[q], free memory
        q += 1


def martelli():
    D = {}  # map composite integers to primes witnessing their compositeness
    q = 2   # first integer to test for primality
    while True:
        p = D.pop(q, None)
        if p:
            x = p + q
            while x in D: x += p
            D[x] = p
        else:
            D[q*q] = q
            yield q
        q += 1


def hochberg():
    yield 2
    D = {}
    q = 3
    while True:
        p = D.pop(q, 0)
        if p:
            x = q + p
            while x in D: x += p
            D[x] = p
        else:
            yield q
            D[q*q] = 2*q
        q += 2


def me():
    yield 2
    D = {}
    q = 3
    while True:
        if q not in D:
            yield q
            D[q*q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p+p+q, []).append(p)
            del D[q]
        q += 2


def test():
    for f in (eppstein, martelli, hochberg, me):
        print(str(f), ':')
        for p in islice(f(), 25):
            print(p, end=' ')
        print()


def speed_test(max_primes=10**6):
    import tqdm

    for f in (eppstein, martelli, hochberg, me):
        print(str(f), ':')
        for p in tqdm.tqdm(islice(f(), max_primes), total=max_primes):
            # print(p, end=' ')
            pass
        print()


def validate(max_primes=10**6):
    reference = list(islice(eppstein(), max_primes))
    for f in (martelli, hochberg, me):
        print(str(f), ':')
        result = list(islice(f(), max_primes))
        print('OK' if result == reference else 'Fail')


if __name__ == '__main__':
    test()
    validate()
    speed_test()

