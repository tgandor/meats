#!/bin/bash

if which avconv ; then
	conv=avconv
else
	conv=ffmpeg
fi

EXT=opus

for f in "$@"; do
	basename="${f%.*}"
	new_name=${basename}.$EXT
	if [ "$f" == "$new_name" ] ; then
		echo "$f - target same as source"
	else
		echo "$f -> $new_name"
		$conv -hide_banner -i "$f" -vn -y "`basename "$new_name"`" 2>&1
	fi
done
