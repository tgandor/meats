#!/usr/bin/env python3

# https://stackoverflow.com/a/16780113/1338797

def f():
    return 1
    yield 2

def g():
    x = yield from f()
    print('yielded from f():', x)

# g is still a generator so we need to iterate to run it:
for _ in g():
    print('g() yielded something:', _)  # this won't print!

