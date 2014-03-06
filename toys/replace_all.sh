#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 search [replace [grepexpr = search]]"
    exit
fi

if [ -z "$2" ]; then
    wcgrep "$1"
    exit
fi

if [ -z "$3" ]; then
    searchexpr="$1"
else
    searchexpr="$3"
fi

if [ -n "$4" ]; then
	condexpr=" if /$4/"
fi

wcgrep -l "$1" | while read f; do echo $f; perl -i -pe "s^$searchexpr^$2^g$condexpr" "$f"; done
