#!/usr/bin/env python

data = [(1, 2), (3, 4)]

# Python 2 OK, python 3 - syntax error
# print(max(data, key=lambda (x, y): x + y))

# missing required argument y / takes exactly 2 arguments 1 given: (2 & 3)
# print(max(data, key=lambda x, y: x + y))

# workaround (1 depth level only, more lambdas required per unpacking level):
print(max(data, key=lambda xy: (lambda x, y: x + y)(*xy)))
