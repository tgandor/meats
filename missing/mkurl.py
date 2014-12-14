#!/usr/bin/env python

import sys

if len(sys.argv) < 2:
    sys.stdout.write("""Usage:
    {0} URL [link_filename[.url]]

- create an Internet shortcut.
""".format(sys.argv[0]))
    exit()

url = sys.argv[1]

if len(sys.argv) == 3:
    target_file = sys.argv[2]
else:
    target_file = url[url.rfind('/')+1:]

if not target_file.endswith('.url'):
    target_file += '.url'

f = open(target_file, 'wb')
f.write('[InternetShortcut]\r\n')
f.write('URL={0}\r\n'.format(url))
f.close()

sys.stdout.write('{0} -> {1}\n'.format(url, target_file))
