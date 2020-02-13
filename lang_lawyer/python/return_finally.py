#!/usr/bin/env python

# See the powers of `finally` clause

def foo():
    try:
        print('Hi from try')
        return
    finally:
        print('Finally has the last word')


foo()

try:
    print('Hi from main program, will soon exit')
    exit()
finally:
    print('But finally still has something to say!')
