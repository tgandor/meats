#!/bin/bash

for f in "$@" ; do
    echo $f
    echo --------------------------------------------
    djpeg -v -v >/dev/null "$f"
    echo --------------------------------------------
done

