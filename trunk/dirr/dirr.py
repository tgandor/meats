#!/usr/bin/env python

import re

def dirr(obj, like=''):
    """Print attributes of object/module etc. matching regular expression."""
    test = re.compile(like, re.IGNORECASE)
    for i in dir(obj):
        if test.search(i):
            print i

def getr(obj, like=''):
    """Return first attribute matching regular expression."""
    test = re.compile(like, re.IGNORECASE)
    for i in dir(obj):
        if test.search(i):
            return getattr(obj, i)


def hlp(obj, like=''):
    """Print help for first attribute matching regular expression."""
    test = re.compile(like, re.IGNORECASE)
    for i in dir(obj):
        if test.search(i):
            help(getattr(obj, i))
            return
