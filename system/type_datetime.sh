#!/bin/bash

# type_date.sh's younger brother

# Unfortunately, binding it to Shift-F8 doesn't work as it should:
# 2019 looks like @)!(
# So something like F7 will be OK.

if ! which xte &> /dev/null ; then
    sudo pacman -S xautomation
fi

xte "str `date '+%Y-%m-%d (%a) %H:%M'`"

