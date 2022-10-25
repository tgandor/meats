#!/bin/bash

# Acknowledgements:
# https://askubuntu.com/questions/410247/how-to-know-last-time-apt-get-update-was-executed
# (not the accepted answer!), this one:  https://askubuntu.com/a/410259/309037
# https://stackoverflow.com/questions/2005021/how-can-i-tell-if-a-file-is-older-than-30-minutes-from-bin-sh

if [ -z  "`find /var/cache/apt/pkgcache.bin -mmin -30`" ] ; then
    echo "Updating..."
    sudo apt update
else
    echo "Package cache relatively fresh."
fi
