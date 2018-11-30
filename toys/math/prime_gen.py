#!/usr/bin/env python

# http://code.activestate.com/recipes/117119/

from __future__ import print_function
from itertools import islice
import argparse


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


def me_pop():
    yield 2
    D = {}
    q = 3
    while True:
        divs = D.pop(q, None)
        if divs:
            for p in divs:
                D.setdefault(p+p+q, []).append(p)
        else:
            yield q
            D[q*q] = [q]
        q += 2


def me_defaultdict1():
    from collections import defaultdict
    yield 2
    D = defaultdict(list)
    q = 3
    while True:
        divs = D.pop(q, None)
        if divs:
            for p in divs:
                D[p+p+q].append(p)
        else:
            yield q
            D[q*q].append(q)
        q += 2


def me_defaultdict2():
    from collections import defaultdict
    yield 2
    D = defaultdict(list)
    q = 3
    while True:
        divs = D.pop(q, None)
        if divs:
            for p in divs:
                D[p+p+q].append(p)
        else:
            yield q
            D[q*q] = [q]
        q += 2


ALL_GENERATORS = [eppstein, martelli, hochberg, me, me_pop, me_defaultdict1, me_defaultdict2]


def test(max_primes=25):
    for f in ALL_GENERATORS:
        print(str(f), ':')
        for p in islice(f(), max_primes):
            print(p, end=' ')
        print()


def speed_test(max_primes=10**6):
    import tqdm

    for f in ALL_GENERATORS:
        print(str(f), ':')
        for p in tqdm.tqdm(islice(f(), max_primes), total=max_primes):
            # print(p, end=' ')
            pass
        print()


def validate(max_primes=10**6):
    reference = list(islice(eppstein(), max_primes))
    for f in ALL_GENERATORS[1:]:
        print(str(f), ':')
        result = list(islice(f(), max_primes))
        print('OK' if result == reference else 'Fail')


def output(max_primes):
    prime_gen = hochberg()
    if max_primes > 0:
        prime_gen = islice(prime_gen, max_primes)
    for p in prime_gen:
        print(p)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--speed', action='store_true')
    parser.add_argument('--validate', action='store_true')
    parser.add_argument('--limit', '-n', type=int, default=10**4)
    args = parser.parse_args()

    if args.test:
        test(args.limit)
        exit()

    if args.validate:
        validate(args.limit)

    if args.speed:
        speed_test(args.limit)

    if not (args.speed or args.validate):
        output(args.limit)

