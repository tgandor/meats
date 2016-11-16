#!/usr/bin/env python

import sys
from fractions import gcd

nums = list(map(int, sys.argv[1:]))

if not nums:
    print('Usage: {} n1 n2 ...'.format(sys.argv[0]))
    exit()

result = nums[0]
for n in nums[1:]:
    result = gcd(result, n)

print('GCD = {}'.format(result))
print(', '.join('{} = {} * {}'.format(n, n/result, result) for n in nums))

