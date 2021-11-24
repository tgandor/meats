#!/bin/bash

if [ "$1" == "-d" ] ; then
    # https://wiki.archlinux.org/title/Pacman/Rosetta
    pacman -Qdtq | sudo pacman -Rs -
else
    pacman -Qdtq | nl | less
fi

