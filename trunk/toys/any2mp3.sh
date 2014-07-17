#!/bin/bash

for f in "$@"; do
	echo "$f -> `basename "$f"`.mp3"
	ffmpeg -loglevel panic -i "$f" -vn -ab 128k -y `basename "$f"`.mp3 2>&1 | grep -v "configuration:" --line-buffered
done
