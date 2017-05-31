
# Python2 needs to derive from `object` for `super(A, self)` to work.

class A(object):
    def __init__(self):
        self.field = 1

    def __setattr__(self, name, value):
        print('Setattr:', name, value)
        super(A, self).__setattr__(name, value)

# expected: constructor assignments use __setattr__

a = A()
print(a.field)
a.field2 = 3

