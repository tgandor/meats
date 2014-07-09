#!/bin/bash

for f in "$@"; do
	echo Converting $f
	sed -i -e 's/[^\r]$/\0\r/g' "$f"
	sed -i -e 's/^$/\r/g' "$f"
done

