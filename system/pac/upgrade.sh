#!/bin/bash

if [ "$1" == "-f" ] ; then
    extra="--overwrite=*"
else
    extra=""
fi

time sudo pacman -Syu $extra
