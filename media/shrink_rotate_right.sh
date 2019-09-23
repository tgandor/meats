#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <file_to_rotate>"
	exit
fi

if which ffmpeg >/dev/null ; then
	converter=ffmpeg
elif which avconv >/dev/null ; then
	converter=avconv
else
	echo Missing either ffmpeg or avconv
	exit 1
fi

infile="$1"
filename=$(basename "$infile")
shift 1

mkdir -p original
mv "$infile" original
mkdir -p converted

time nice $converter -i "original/$filename" -vf transpose=1 -s 504x900 -c:a copy -preset veryslow -map_metadata 0 -crf 23 "$@" "converted/$filename"

