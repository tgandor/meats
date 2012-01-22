#!/bin/bash

if [ -z $1 ]; then
	echo "Usage: $0 executable [executable...]"
	echo "Scans the PATH variable for writable dirs, and tries to symlink target(s)"
	echo "on the first writable directory."
	echo "Set FORCE variable to overwrite any current symlink."
	exit
fi

for f in $@; do
	basename=`basename $f`
	realpath=`readlink -f $f`
	if which $basename && [ -z $FORCE ] ; then
		echo "$basename already linked:" `which $basename`
		continue
	fi
	OIFS=$IFS
	IFS=:
	for p in $PATH; do
		if [ -w $p ]; then
			echo "$p - writable, linking to $p/$basename."
			if [ -e "$p/$basename" ]; then
				echo "Link exists: $p/$basename ->" `readlink -f "$p/$basename"`
				echo "removing..."
				rm "$p/$basename"
			fi
			ln -s "$realpath" "$p/$basename"
			break
		else
			echo "$p - not writable"
		fi
	done
	IFS=$OIFS
done

