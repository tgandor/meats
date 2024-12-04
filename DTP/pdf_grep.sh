#!/bin/bash

greparg="$1"
shift

if [ "$2" == "" ]; then
    for pdffile in "$@"; do
        pdftotext -layout "$pdffile" - | grep "$greparg" | sed -E "s/ +/ /g" | sed "s/^ //"
    done
else
    for pdffile in "$@"; do
        echo "--- $pdffile ---"
        pdftotext -layout "$pdffile" - | grep "$greparg" | sed -E "s/ +/ /g" | sed "s/^ //"
    done
fi
