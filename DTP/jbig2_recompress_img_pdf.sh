#!/bin/bash

# See:
# https://github.com/agl/jbig2enc

if [ "$1" == "" ] ; then
    echo "Usage: $0 <IMAGE_FILES>"
    exit
fi

if ! which jbig2 ; then
    echo "Missing JBIG2 encoder. Trying to build."
    pamac build jbig2enc
fi

if ! which python2 ; then
    echo "Missing python 2 -- pdf.py needs it."
    exit
fi

jbig2 -s -p -v "$@" && pdf.py output > out.pdf
