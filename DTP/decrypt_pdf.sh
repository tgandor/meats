#!/bin/bash

if which qpdf ; then
    read -p "Password:" passwd
    qpdf --password="$passwd" --decrypt "$1" "decrypted_$1"
    exit
fi

echo "Missing, please install qpdf."
