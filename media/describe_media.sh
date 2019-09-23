#!/bin/bash

for i in "$@"; do
	echo $i
	ffmpeg -i "$i" 2>&1 | grep creation_time\\\|Duration\\\|Stream | sed 's/^ *//' |  sort | uniq
	echo "---"
done
