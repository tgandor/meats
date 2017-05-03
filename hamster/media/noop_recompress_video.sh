#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <file_to_recompress> [options]"
	echo "Option example: -vf transpose=1 -s 960x540 etc."
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
shift 1
mkdir -p original
mkdir -p converted
mv "$infile" original

time nice $converter -i "original/$infile" "$@" -c:a copy -map_metadata 0 -crf 26 -preset veryslow "converted/$infile"
