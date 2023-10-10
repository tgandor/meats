#!/bin/bash

if [ "$Q" == "" ] ; then
    echo "Not specifying quality, use Q=<quality> to set."
else
    Q="-quality $Q"
fi


if [ "$R" == "" ] ; then
    echo "Not specifying resize, use R=<geometry> to set."
else
    R="-resize $R"
fi
time parallel convert -verbose -auto-orient $Q $R {} {.}.webp ::: "$@"
