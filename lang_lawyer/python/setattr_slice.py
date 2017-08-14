from __future__ import print_function


class Magic(object):
    def __setattr__(self, attr, value):
        print('Settattr called:', attr, value)
        super(Magic, self).__setattr__(attr, value)

    def __init__(self, f=[]):
        self.f = f

m = Magic([2, 1])
m.f = [1, 2]

m.f[:] = [2, 1]  # Yes, this does not print

