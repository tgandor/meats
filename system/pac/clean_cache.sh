#!/bin/bash

# https://unix.stackexchange.com/questions/137320/how-to-delete-old-packages-installed-by-pacman-in-arch-linux
# https://forum.manjaro.org/t/how-to-remove-pamac-aur-build-files-in-var-tmp-pamac-build-username/122077

if [ "$1" == "--all" ] ; then
    echo "Checking all cache (no last version kept)"
    paccache --keep 0 --remove
else
# agressive, but last versions are still kept
# use --keep 0 to free up a few more gigs still.
    paccache --keep 1 --remove
fi

sudo pamac clean -b --no-confirm
