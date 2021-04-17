#!/bin/bash

if [ "$1" == "" ] ; then
    days=7
else
    days=$1
fi

find -newermt "$days days ago"

