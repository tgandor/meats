#!/bin/bash

# When you live with admins bad,
# broken(*) SSL who had.

# (*) - broken != cracked. They're just the man-in-the-middle.

# https://stackoverflow.com/questions/25981703/pip-install-fails-with-connection-error-ssl-certificate-verify-failed-certi
# Other interesting options:
# pip --cert /etc/ssl/certs/FOO_Root_CA.pem "$@"
# but:
# "config --global http.sslVerify false" doesn't work!

python -m pip --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -vvv "$@"

