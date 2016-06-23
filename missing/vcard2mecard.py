#!/usr/bin/env python

import os
import sys

try:
    import vobject
except ImportError:
    print('Missing vobject module')
    res = os.system('sudo apt-get install python-vobject')
    print('Please rerun')
    exit()


def vcards(vcard_file):
    with open(vcard_file) as f:
        while True:
            yield vobject.readOne(f)


def sanitize_n_valueRepr(nvr):
    # return nvr.strip().split('  ')[::-1]  # Surname,Name
    return nvr.strip().replace('  ', ' ')  # Just strip & remove double space

for vcard_file in sys.argv[1:]:
    for vcard in vcards(vcard_file):
        print('MECARD:N:{};FN:{};TEL:{};;'.format(
            sanitize_n_valueRepr(vcard.n.valueRepr()),
            vcard.fn.value,
            vcard.tel.value
        ))
