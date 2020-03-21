#!/bin/bash

# https://unix.stackexchange.com/questions/137320/how-to-delete-old-packages-installed-by-pacman-in-arch-linux

if [ "$1" == "--all" ] ; then
    echo "Checking all cache (no last version kept)"
    paccache --keep 0 --remove
else
# agressive, but last versions are still kept
# use --keep 0 to free up a few more gigs still.
    paccache --keep 1 --remove
fi


