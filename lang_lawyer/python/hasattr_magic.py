
class Magic:
    def __init__(self):
        self.real_attr = 1

    def __getattr__(self, item):
        if item == 'magic_attr':
            return 2
        raise AttributeError


def check_attr(obj, name):
    """
    Call hasattr on obj.

    >>> m = Magic()
    >>> check_attr(m, 'real_attr')
    True
    >>> check_attr(m, 'magic_attr')
    True
    >>> check_attr(m, 'no_attr')
    False
    """
    return hasattr(obj, name)


m = Magic()
print(hasattr(m, 'real_attr'))
print(hasattr(m, 'magic_attr'))
print(hasattr(m, 'no_attr'))
