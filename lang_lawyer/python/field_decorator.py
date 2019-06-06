# Take home: no syntactic sugar for that exists as of now.

def method_decorator(method):
    print('method_decorator: ', method)
    print('method_decorator (__name__): ', method.__name__)
    return method

def field_decorator(field):
    print('field_decorator:', field)
    return field

class Something:
    @method_decorator
    def foo(self, bar):
        return bar

    # Sorry, all syntax errors:

    # @field_decorator
    # x : int

    # @field_decorator
    # x

    # This is a common pattern:

    x = field_decorator('x')
