from __future__ import print_function

class slicer:
    def __getitem__(self, item):
        print(type(item), ':', repr(item))

s = slicer()

s[1]
s[:]
s[0:5, -2:]
s[...]

