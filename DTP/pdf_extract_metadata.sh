#!/bin/bash

if ! which pdftk >/dev/null; then
    sudo snap install pdftk
fi

# this seems to not work for many a PDF
# (and not very exotic - just plain LibreOffice generated)

for i in "$@" ; do
    echo pdftk "$i" dump_data output `basename "$i" .pdf`_meta.txt
done
