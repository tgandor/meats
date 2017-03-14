
from __future__ import print_function
from collections import namedtuple

Point = namedtuple('Point', 'x y')

def print_args(*args):
    print(args)

p = Point(2, 3)
print_args(*p)

