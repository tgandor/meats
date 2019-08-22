"""
all() and any() builtins do short-circuit on generators.
"""

def bool_generator():
    for _ in range(2):
        print('passing False')
        yield False

    print('passing True')
    yield True

    for _ in range(2):
        print('passing False after')
        yield False


if any(bool_generator()):
    print('done with any(bool_generator())')

if all(x for x in bool_generator()):
    print('it never prints')

print('done with all(genexpr)')

# ever wondered what they do on empty iterables?

print('all([]): ', all([]))  # True
print('any([]): ', any([]))  # False

# all() is a product,
# any() is a sum.
