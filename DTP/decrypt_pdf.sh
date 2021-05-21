#!/bin/bash

if which qpdf ; then
    read -s -p "Password:" passwd
    qpdf --password="$passwd" --decrypt "$1" "decrypted_$1"
    exit
fi

echo "Missing, please install qpdf."
