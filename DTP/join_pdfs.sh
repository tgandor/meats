#!/bin/bash

if ! which pdftk ; then
    echo "Missing pdftk, trying to install"
    sudo snap install pdftk
fi

pdftk "$@" cat output joined.pdf
