#!/bin/bash

if [ "$1" == "" ] ; then
    n=""
else
    n="-n $1"
fi

grep -o '\w\+' | sort | uniq -c | sort -n -r | head $n
