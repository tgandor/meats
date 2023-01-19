#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <file_to_rotate>"
	echo "NOTE: 'metadata' rotation, for re-coding see recompress_to_mp4.py"
	exit
fi

mkdir -p original
mv "$1" original

# previous, recoding options:
# -vf transpose=1,transpose=1 - also OK
# time ffmpeg -i "original/$1" -vf vflip,hflip -c:a copy "$1"
time ffmpeg -i "original/$1" -map_metadata 0 -metadata:s:v rotate="180" -codec copy "$1"
