#!/bin/bash

if which qpdf ; then
    read -s -p "Password:" passwd
    echo
    qpdf --encrypt "$passwd" "$passwd" 256 --  "$1" "crypted_$1"
else
    echo "Missing, please install qpdf."
fi
