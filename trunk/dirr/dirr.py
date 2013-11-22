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
    return None

def hlp(obj, like=''):
    """Print help for first attribute matching regular expression."""
    test = re.compile(like, re.IGNORECASE)
    for i in dir(obj):
        if test.search(i):
            help(getattr(obj, i))
            return True
    return False

def interactive():
    modules = []
    try:
        while True:
            cmd = raw_input()
            if cmd == 'q':
                break
            if cmd.startswith('i '):
                modules.append(__import__(cmd[2:]))
                print "Loaded modules:", ", ".join([m.__name__ for m in modules])
            elif cmd.startswith('h '):
                for m in modules:
                    if hlp(m, cmd[2:]):
                        break
            else:
                for m in modules:
                    if getr(m, cmd) is not None:
                        print "  ---  In module %s:  ---  " % (m.__name__,)
                        dirr(m, cmd)
    except EOFError:
        pass
    print "Be seeing you..."

if __name__ == '__main__':
    interactive()
