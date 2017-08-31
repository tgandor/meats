from __future__ import print_function

valid = {'a', 'b', 'c'}

tested1 = ['b', 'c', 'd']
tested2 = ['b', 'c']


def fun_with_valid(tested):
    for v in tested:
        if v not in valid:
            print('In:', tested, ' - Value invalid:', v)
            break
    else:
        print('All values passed:', tested)

fun_with_valid(tested1)
fun_with_valid(tested2)

