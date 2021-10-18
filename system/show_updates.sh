#!/bin/bash

# Old Debian / Ubuntu, before `apt` command:
# apt-get --just-print upgrade | egrep -v '^Inst |^Conf '

# Debian / Ubuntu
if which apt &> /dev/null ; then
    apt list --upgradable | tail -n+2 | cut -d/ -f1 | nl | less
fi

# Arch / Manjaro (pacman)
# please note: pacman -Qu shows nothing when Octopi reports new updates.
if which checkupdates &> /dev/null ; then
    checkupdates | nl | less
fi
