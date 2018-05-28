#!/bin/bash

# this is a counterpart to create_safer_volume.sh

if [ -z "$1" ] ; then
    file=image_.bin
else
    file="$1"
fi

echo "Unmounting"
sudo umount /dev/mapper/$file

echo "Closing file $file"
sudo cryptsetup close $file

echo "Removing mount point /mnt/$file"
sudo rmdir /mnt/$file

