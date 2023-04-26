#!/bin/bash

if [ -z "$VIRTUAL_ENV" ] ; then
    echo "Not in a virtualenv. Please activate one."
    exit
fi

python -m ipykernel install --user --name=$(basename $VIRTUAL_ENV) --display-name=$(basename $VIRTUAL_ENV)

