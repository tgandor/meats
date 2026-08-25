#!/bin/bash

for f in "$@" ; do
    echo $(date) starting "$f"
    time ffmpeg -v warning -i "$f" -f null -
    echo $(date) finished "$f"
done
