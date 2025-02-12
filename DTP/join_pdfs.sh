#!/bin/bash

if ! which pdftk ; then
    echo "Missing pdftk, trying to install"
    sudo apt install pdftk-java
fi

pdftk "$@" cat output joined.pdf
