#!/usr/bin/env python

# for nginx see here: 
# https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/

import base64
import os
import getpass
import hashlib
import sys

try:
    import readline
except:
    pass

if os.path.exists('.htaccess'):
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

auth_name = input('AuthName (Please login): ')
if not auth_name:
    auth_name = 'Please login'

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
