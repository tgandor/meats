#!/bin/bash

# https://www.kernel.org/doc/Documentation/security/Yama.txt

if [ -z "$1" ] ; then

if [ $(cat /proc/sys/kernel/yama/ptrace_scope) == "1" ] ; then
	echo "Unlocking ptrace, may ask for pass."
	echo 0 |sudo tee /proc/sys/kernel/yama/ptrace_scope
else
	echo "ptrace is already unlocked."
fi

else  # $1 != "", eg. off, lock etc.

if [ $(cat /proc/sys/kernel/yama/ptrace_scope) == "0" ] ; then
	echo "Locking ptrace, may ask for pass."
	echo 1 |sudo tee /proc/sys/kernel/yama/ptrace_scope
else
	echo "ptrace is already locked."
fi

fi
