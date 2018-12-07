#!/bin/bash

missing=""
if ! which pdfimages >/dev/null; then
    missing="$missing poppler-utils"
fi
if [ -n "$missing" ] ; then
    echo "Missing packages: $missing"
    sudo apt-get install $missing
fi

for i in "$@" ; do
    echo $i
    pdfimages -j "$i" "`basename "$i" .pdf`"
done
