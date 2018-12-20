#!/usr/bin/env python

import argparse


def factorize(n):
    d = 2
    while n > 1:
        power = 0
        while n % d == 0:
            n = n // d
            power += 1
        if power:
            yield (d, power)
        d += 1


def divisor_count(factorization):
    product = 1

    for _, power in factorization:
        product *= (power + 1)

    return product - 2


def divisor_sum(factorization):
    product = 1

    for p, power in factorization:
        product *= sum(p ** k for k in range(power + 1))

    return product


def _format_factor(prime, power):
    if power > 1:
        return '({} ** {})'.format(prime, power)
    return str(prime)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    args = parser.parse_args()

    factors = list(factorize(args.n))
    print('n = {}'.format(' * '.join(_format_factor(prime, power) for prime, power in factors)))
    print('proper divisor count: {:,}'.format(divisor_count(factors)))
    print('divisor sum: {:,}'.format(divisor_sum(factors)))

