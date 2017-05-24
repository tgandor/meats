from __future__ import print_function


class Addable:
    def __add__(self, arg):
        print('Addable.__add__({})'.format(arg))
        return self

a = Addable()
a + 0
a += 1


class AugumentedAddable:
    def __iadd__(self, arg):
        print('AugumentedAddable.__iadd__({})'.format(arg))
        return self

aa = AugumentedAddable()
aa += 2
aa + 3

