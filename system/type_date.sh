#!/bin/bash

# with thanks to:
# https://unix.stackexchange.com/a/39277/98519
# I just prefer ISO format ;)

# One gotcha - bind it to something without the modifiers (Alt, Ctrl),
# because it will be interpreted as Ctrl+2 + ... (rest of the date).
# So something like F8 will be OK.

if ! which xte &> /dev/null ; then
    sudo pacman -S xautomation
fi

xte "str `date --iso`"

