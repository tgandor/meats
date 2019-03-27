#!/bin/bash

if ! which pdfimages >/dev/null; then
    sudo apt install poppler-utils
fi

for i in "$@" ; do
    echo $i
    pdfimages -j "$i" "`basename "$i" .pdf`"
done
