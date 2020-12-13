#!/usr/bin/env python

# extended euclid algorithm in steps
# letters: m, n, (args), a, a1, b, b1, c, d  - like in AoCP 1.2.1 algorithm E

# function from Wikipedia or something:


def gcd_extended_euclid(x, y):
    r0, r1 = x, y  # c, d = m, n
    u0, u1 = 1, 0  # a1, a = 1, 0
    v0, v1 = 0, 1  # b1, b = 0, 1

    while r1 > 0:  # while d > 0 (1 iteration more)
        qi = r0 // r1
        assert u0 * x + v0 * y == r0  # this holds here
        assert u1 * x + v1 * y == r1  # and then after - in next iteration
        r0, r1 = r1, r0 - qi * r1  # c, d = d, d - q*c
        u0, u1 = u1, u0 - qi * u1
        v0, v1 = v1, v0 - qi * v1

    return r0, u0, v0  # c, a1, b1 - one iteration later


import sys

m, n = map(int, sys.argv[1:])

a1 = b = 1
a = b1 = 0
c = m
d = n

print('\t'.join('a1 a b1 b c d q r'.split()))

while True:
    q = c // d
    r = c % d

    print('\t'.join(str(x) for x in (a1, a, b1, b, c, d, q, r)))

    assert a*m + b*n == d and a1*m + b1*n == c and c == q*d + r, "A3"

    if r == 0:
        break

    # c = d
    # d = r
    c, d = d, r

    # t = a1
    # a1 = a
    # a = t - q*a
    a1, a = a, a1 - q*a

    # t = b1
    # b1 = b
    # b = t - q*b
    b1, b = b, b1 - q*b

    assert a*m + b*n == d and a1*m + b1*n == c, "A6"

    # print('am + bn = d : {}*{} + {}*{} = {}'.format(a, m, b, n, d))

print('am + bn = d : {}*{} + {}*{} = {}'.format(a, m, b, n, d))
print(gcd_extended_euclid(m, n))
