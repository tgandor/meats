#!/bin/bash

sudo apt-get install cups cups-bsd samba
sudo usermod -a -G lpadmin pi

echo Probably need to logout and login before configuring:
echo http://localhost:631

echo TODO: maybe configure /etc/samba/smb.conf for Samba sharing
echo BUT, samba should be installed, and shared printers (in CUPS) should be visible.
