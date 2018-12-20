class Base1(object):
    def amethod(self): print("Base1")

class Base2(Base1):
    pass

class Base3(object):
    def amethod(self): print("Base3")

class Derived(Base2, Base3):
    pass

instance = Derived()
instance.amethod()
print((Derived.__mro__))
