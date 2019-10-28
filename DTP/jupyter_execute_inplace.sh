#!/bin/bash

# again, just to remember

if ! which jupyter > /dev/null ; then
    echo "Missing jupyter"
    echo "Install or activate the environment"
fi

jupyter nbconvert --execute --to notebook --inplace "$1"
