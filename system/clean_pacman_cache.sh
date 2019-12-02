#!/bin/bash

# https://unix.stackexchange.com/questions/137320/how-to-delete-old-packages-installed-by-pacman-in-arch-linux

# agressive, but last versions are still kept
# use --keep 0 to free up a few more gigs still.

paccache --keep 1 --remove

