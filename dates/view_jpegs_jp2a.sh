#!/bin/bash

# very primitive, BTW:

if ! which jp2a >/dev/null; then
    sudo apt install jp2a
fi

for i in *.jpg; do jp2a "$i"; read ; done
