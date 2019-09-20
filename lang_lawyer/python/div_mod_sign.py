print('(n, (n // 3, n % 3), (n // -3, n % -3))')

for i in range(-6, 7):
    print((i, divmod(i, 3), divmod(i, -3)))

"""
Results:
(floor division - towards -inf, modulus = dividend - result * divisor, e.g.:
2 % (-3) == 2 - (-1) * (-3) == 2 - 3 == -1)

This means that the modulus has the sign of the DIVISOR.

but: (!!!)

modulus != sign(divisor) * (abs(dividend) % abs(divisor))

(-6, (-2, 0), (2, 0))
(-5, (-2, 1), (1, -2))
(-4, (-2, 2), (1, -1))
(-3, (-1, 0), (1, 0))
(-2, (-1, 1), (0, -2))
(-1, (-1, 2), (0, -1))
(0, (0, 0), (0, 0))
(1, (0, 1), (-1, -2))
(2, (0, 2), (-1, -1))
(3, (1, 0), (-1, 0))
(4, (1, 1), (-2, -2))
(5, (1, 2), (-2, -1))
(6, (2, 0), (-2, 0))
"""

