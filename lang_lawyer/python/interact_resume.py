#!/usr/bin/env python

import code
import os

try:
    for i in range(5):
        print(i)
        val = input('enter something: ')
        print('you entered:', val)
        code.interact(
            banner='Welcome to interact. send EOF to continue, call '
                   'exit() to finish this process.',
            local=locals(),
            exitmsg='So, you managed to get out and continue.',
        )
except SystemExit:
    print('Exiting because of SystemExit')
    # probably no more interaction:
    # val = input('enter something, last time: ')
    # -> ValueError: I/O operation on closed file.
    # print('you entered:', val)

