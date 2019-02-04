#!/bin/bash

# this tiny script tries to add its directory to the path
# the problem is - it cannot modify the PATH for the parent
# so it adds it to .bashrc
# Changes take effect on next shell start

mydir=`dirname $0`
mydir=`realpath $mydir`

if echo $PATH | grep -q "$mydir"; then
    echo "$mydir already on PATH"
elif grep -q "$mydir" ~/.bashrc ; then
    echo "$mydir in .bashrc PATH, restart the shell"
else
    echo "PATH=\$PATH:$mydir" | tee -a ~/.bashrc
    echo "$mydir added to PATH in .bashrc; restart the shell"
fi
