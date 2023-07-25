#!/usr/bin/env python


def print_name(f):
    print("Decorated function:", f.__name__, f)


@print_name
def foo(x=5):
    pass


@print_name
def bar():
    pass
