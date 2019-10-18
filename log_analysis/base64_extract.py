#!/usr/bin/env python

import base64
import re
import sys

b64_regex = re.compile(
    r'^(?:[A-Za-z0-9+/]{4})+(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})\s*$',
    re.MULTILINE
)

input_data = sys.stdin.read()
suffix = '.png'

for i, match in enumerate(b64_regex.finditer(input_data)):
    s = match.span()
    print(i, match, '({:,} characters)'.format(s[1] - s[0]))
    data = match.group().encode()
    out_filename = 'b64_decoded_{}{}'.format(i, suffix)
    with open(out_filename, 'wb') as out_file:
        decoded = base64.decodebytes(data)
        out_file.write(decoded)
    print('{:,} decoded bytes written to {}'.format(len(decoded), out_filename))
    print('---')
