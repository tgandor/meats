#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <file_to_rotate>"
	exit
fi

mkdir -p original
mv "$1" original

# -vf transpose=1,transpose=1 - also OK
time avconv -i "original/$1" -vf vflip,hflip -c:a copy "$1"
