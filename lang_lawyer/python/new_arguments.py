class Foo(object):
    def __new__(cls, *args, **kwargs):
        print("Creating Instance", args, kwargs)
        # instance = super(Foo, cls).__new__(cls, *args, **kwargs)
        # gives:
        # TypeError: object.__new__() takes exactly one argument (the type to instantiate)
        instance = super(Foo, cls).__new__(cls)
        return instance

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def bar(self):
        pass

i = Foo(2, 3)
print(i)


