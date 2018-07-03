#!/usr/bin/env python3

from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float
    z: float

# AttributeError: Cannot overwrite NamedTuple attribute __init__
#    def __init__(self, x, y, z=0.0):
#        self.x = x
#        self.y = y
#        self.z = z

# TypeError: __new__() missing 1 required positional argument: 'z'
# p = Point(1, 2)

# No way around it so far:
p = Point(1, 2, 3)
print(p)
