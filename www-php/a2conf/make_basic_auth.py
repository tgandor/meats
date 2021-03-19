#!/usr/bin/env python

# for nginx see here: 
# https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/

import argparse
import base64
import getpass
import hashlib
import os
import sys

try:
    import readline
except:
    pass

parser = argparse.ArgumentParser()
parser.add_argument('--force', '-f', action='store_true')
parser.add_argument('--auth-name', '-n')
args = parser.parse_args()

if os.path.exists('.htaccess') and not args.force:
    print('.htaccess exists; exiting')
    exit()

template = """
Authtype Basic
AuthName "{}"
AuthUserFile {}/.htpasswd
Require valid-user
"""

if sys.version_info[0] == 2:
    input = raw_input

if not args.auth_name:
    auth_name = input('AuthName (Please login): ')
    if not auth_name:
        auth_name = 'Please login'
else:
    auth_name = args.auth_name

with open('.htaccess', 'w') as f:
    f.write(template.format(auth_name, os.getcwd()))

with open('.htpasswd', 'w') as f:
    while True:
        username = input('Username (empty to quit): ')
        if not username:
            break
        password = getpass.getpass()
        password_hash = base64.b64encode(hashlib.sha1(password).digest())
        f.write('%s:{SHA}%s\n' % (username, password_hash))

print('-' * 40)
print('Apache configuration directives:')
print(template.format(auth_name, os.getcwd()))
print('-' * 40)
print('NginX configuration directives:')
print("""
auth_basic "{}";
auth_basic_user_file "{}/.htpasswd";
""".format(auth_name, os.getcwd()))
