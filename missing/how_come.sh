#!/bin/bash

if [ "$1" == "" ]; then
	echo "Usage: $0 <command>"
	echo "Prints package and apt-get command for installing it."
	exit
fi

if ! which $1; then
	echo "Command not found."
	exit
fi

cmd_path=`which $1`

# sometimes a command is symlinked via alternatives:
real_path=`readlink -f $cmd_path`
if [ "$real_path" != "$cmd_path" ] ; then
    # special case: snaps
    if [ "$real_path" == "/usr/bin/snap" ] ; then
        echo "This comes from a snap package"
        echo "Probably just:"
        echo "sudo snap install $1"
        exit
    fi

    echo "$real_path"
    cmd_path=$real_path
fi

dpkg -S $cmd_path | awk '{ gsub(/:$/, "", $1); print "sudo apt install " $1;}'
echo "---"
echo 'missing=""'
dpkg -S $cmd_path | awk '{ gsub(/:$/, "", $1); print "if ! which '$1' >/dev/null; then\n\tmissing=\"$missing " $1 "\"\nfi"; }'

echo 'if [ -n "$missing" ] ; then'
echo '    echo "Missing packages: $missing"'
echo '    sudo apt install $missing'
echo 'fi'

