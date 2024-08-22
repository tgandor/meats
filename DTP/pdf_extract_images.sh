#!/bin/bash

if ! which pdfimages >/dev/null; then
    sudo apt install poppler-utils
    sudo pacman -S poppler
fi

format="-j"
if [ "$1" == "-png" ] ; then
    format="-png"
    shift
fi

for i in "$@" ; do
    echo $i
    pdfimages $format "$i" "`basename "$i" .pdf`"
done
