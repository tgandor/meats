
# Only 3.x - probably needs new style classes?

# Well, no. 2.7 gives the very same results.


class A:
    def util(self):
        print('Original method')

    def interface(self):
        self.util()


class B(A):
    def util(self):
        print('Overriden method')


B().interface()  # Overriden method, as expected.


class C:
    def interface(self):
        self.__util()

    def util(self):
        print('Original method')

    __util = util  # this local copy needs two underscores, a single doesn't work


class D(C):
    def util(self):
        print('Overriden method')

    # works despite this below:
    __util = util


D().interface()  # Original method
