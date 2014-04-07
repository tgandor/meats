#!/bin/bash
for i in "$@"; do
	echo "Showing $i..."
	qrencode "$i"  -o -| display -resize 300x300% -
done
