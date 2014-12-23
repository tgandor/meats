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


dpkg -S $cmd_path | awk '{ gsub(/:$/, "", $1); print "sudo apt-get install " $1;}'
echo "---"
echo 'missing=""'
dpkg -S $cmd_path | awk '{ gsub(/:$/, "", $1); print "if ! which '$1' >/dev/null; then\n\tmissing=\"$missing " $1 "\"\nfi"; }'

echo 'if [ -n "$missing" ] ; then'
echo '    echo "Missing packages: $missing"'
echo '    sudo apt-get install $missing'
echo 'fi'

