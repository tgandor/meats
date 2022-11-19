#!/bin/bash

# somewhat based on: https://askubuntu.com/questions/302188/certificate-error-when-using-citrix-receiver
# but Mozilla has no pems anymore.

sudo cp /etc/ssl/certs/*.pem /opt/Citrix/ICAClient/keystore/cacerts
sudo /opt/Citrix/ICAClient/util/ctx_rehash
