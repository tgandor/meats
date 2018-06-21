from abc import abstractmethod


class Interface:
    # inspections warn about no __init__ method
    @abstractmethod
    def foo(self):
        raise NotImplementedError

    @abstractmethod
    def bar(self):
        raise NotImplementedError


class Implementation(Interface):
    # inspections warn about not overriding all abstract methods
    def foo(self):
        print('Foo works')


impl = Implementation()  # this is not C++, a class with abstract methods can be created
impl.foo()
impl.bar()
