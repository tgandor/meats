#!/bin/bash

if ! which jupyter > /dev/null ; then
    echo "Missing jupyter"
    echo "Install or activate the environment"
fi

jupyter nbconvert "$1" --to slides --post serve
