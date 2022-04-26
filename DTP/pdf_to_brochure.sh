#!/bin/bash

if ! which pdfbook2 ; then
    echo "Missing pdfbook2"
    echo "sudo pacman -S texlive-core"
    echo "sudo apt install texlive-extra-utils"
    echo "Or look for alternatives: pdfbook, pdfjam or ... boomaga."
    exit
fi

echo "Use short-edge double sided printing."
pdftk -s "$@"
