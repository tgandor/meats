#!/bin/bash

# This script drops a swapfile created by add_extra_swap.sh
# first argument (size) is ignored

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


echo "Current swap situation:"
swapon --show
df $file
echo "Unswapping off of $file, please wait... (This may take forever if full, speed e.g. ~10 MB/s)"
sudo swapoff $file
sudo rm $file
echo "After unswapping:"
swapon --show
df `dirname $file`
