#!/bin/bash

if [ "$1" == "" ] ; then
    echo "Usage: $0 pacman-<date>.tar"
    exit
fi

tar_path=`realpath $1`
cd /
sudo tar xvf "$tar_path"
echo "Finished unpacking $tar_path"
echo "You can now run:"
echo "~/meats/system/pac/upgrade.sh"
