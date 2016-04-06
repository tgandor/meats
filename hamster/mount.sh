#!/bin/bash

cd `dirname $0`

if grep `pwd`/mnt /proc/mounts ; then
    echo "Already mounted, exiting"
    exit
fi

if [ ! -d mnt ] ; then
    echo "Creating directory mnt/"
    mkdir mnt
fi

jmtpfs mnt

