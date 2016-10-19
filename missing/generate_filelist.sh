#!/bin/bash

if [ -z "$1" ] ; then
    target=filelist.txt
else
    target=$1
fi

time find -type f | while read f; do
    md5sum "$f" >> "$target"
    echo $f
done
