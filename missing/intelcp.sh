#!/bin/bash

if [ -z "$2" ]; then
	if [ -z "$1" ]; then
		echo 'missing destination file operand'
	else
		echo "missing file operand(s) after $1"
	fi
	echo 'Usage: intelcp.sh DEST [OPTION] SOURCE...'
	exit
fi

target_path=$1
shift

cp "$@" "$target_path"
