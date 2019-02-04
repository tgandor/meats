
from __future__ import print_function

class A:
    def f(self):
        pass

    def g(self):
        pass


class B:
    def f(self):
        # overriden
        pass

    def h(self):
        pass

import inspect

a = inspect.getmembers(A)
# print(a)
b = inspect.getmembers(B)
# print(b)

for k, v in b:
    if k.startswith('__'):
        continue
    if k not in a or v != b[k]:
        print('Not inherited:', k, v)

