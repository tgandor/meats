#!/bin/bash

for f in "$@" ; do
    echo $f
    echo --------------------------------------------
    # this is so dumb (completely counterintuitive order of redirects)
    # https://stackoverflow.com/questions/12027170/shell-redirect-stdout-to-dev-null-and-stderr-to-stdout
    # https://stackoverflow.com/questions/2342826/how-to-pipe-stderr-and-not-stdout

    # BTW, this is sou dumb. Could have also been 2>&3 1>/dev/null 3>&1 ?
    # no, other way round:
    # 3>&1 1>/dev/null 2>&3; because x>&y is like stream *x, *y; x = &(*y);
    # i.e., where it "points to"

    djpeg -v -v 2>&1 1>/dev/null "$f" | grep 'Define Quantization' -A8
    echo --------------------------------------------
done
