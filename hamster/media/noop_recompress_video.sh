#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <file_to_recompress> [options]"
	echo "Option example: -vf transpose=1 -s 960x540 etc."
	exit
fi

infile="$1"
shift 1
mkdir -p original
mv "$infile" original

time avconv -i "original/$infile" "$@" -c:a copy "$infile"
