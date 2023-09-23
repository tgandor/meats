#!/bin/bash

if [ "$1" == "" ] ; then
    # get root device
    device=`mount | awk '/on \/ type/{print $1}'`
else
    device=$1
fi

sudo hdparm -t --direct $device
