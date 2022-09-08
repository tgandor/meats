#!/bin/bash

if ! id | grep -q docker ; then
    prefix='sudo'
fi

if [ "$1" == "" ] ; then
    image=ubuntu
else
    image="$1"
    shift
fi

if [ "$1" == "" ] ; then
    command=bash
else
    command="$@"
    shift
fi

$prefix docker run --rm -it $image $command
