#!/bin/bash

if [ "$1" == "" ] ; then
    find -xtype l | tee /dev/tty | grep -q . \
    && echo "Pass any argument (e.g. -x) to delete broken links." || echo "Nothing found."
else
    echo "Cleaning:"
    find -xtype l -print -exec rm {} \;
    echo "Done."
fi
