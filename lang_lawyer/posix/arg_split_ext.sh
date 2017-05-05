#!/bin/bash

for fullfile in "$@" ; do
	filename=$(basename "$fullfile")
	extension="${filename##*.}"
	filename="${filename%.*}"
	echo "Filename: $filename | extension: $extension"
done

if [ "$1" == "" ] ; then
	echo "Usage: $0 filename..."
fi
