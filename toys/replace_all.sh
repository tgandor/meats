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
    grexpr="$1"
else
    grexpr="$3"
fi

wcgrep -l "$grexpr" | while read f; do echo $f; perl -i -pe "s/$1/$2/g" "$f"; done

