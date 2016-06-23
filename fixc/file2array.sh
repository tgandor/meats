#!/bin/bash

if [ -z "$1" ]; then
	echo 'Usage file2array.sh BINARY_FILE [ARRAY_NAME]'
	exit
fi

if [ -z "$2" ]; then
	xxd -i "$1" | sed 's/unsigned/const unsigned/' > "$1".c
else
	cp -i "$1" "$2"
	xxd -i "$2" | sed 's/unsigned/const unsigned/' > "$2".c
	rm "$2"
fi
