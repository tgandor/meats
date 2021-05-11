#!/bin/bash

echo "Press Ctrl-C to break the cycle."

if [ -z "$1" ] ; then
    echo "Usage: $0 <file_or_directory_to_watch> command_to_execute [ args ... ]"
    exit
fi

target=$1
shift

while true; do
    inotifywait $target
    "$@"
done
