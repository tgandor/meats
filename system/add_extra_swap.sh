#!/bin/bash

# This script creates a swapfile (/tmp/swapfile by default) with as many GB as specified.
# (10 GB by default)

if [ -z "$1" ] ; then
    gb=10
else
    gb=$1
fi

if [ -z "$2" ] ; then
    file=/tmp/swapfile
else
    file="$2"
fi

# this won't work, fails with:
# swapon: /tmp/swapfile: skipping - it appears to have holes.
# sudo dd if=/dev/zero of=$file bs=1G count=0 seek=$gb

free -m
df `dirname $file`
echo "Creating $gb GB of zeros in $file, please wait..."
sudo dd if=/dev/zero of=$file bs=1G count=$gb
sudo chmod 600 $file
sudo mkswap $file
sudo swapon $file
echo "After swapping"
df $file
swapon --show
free -m
echo "Swappiness: `cat /proc/sys/vm/swappiness`"
