#!/bin/bash

find -type d -name .git | while read d; do
    echo "--------------"
    echo "${d%/.git}"
    echo "--------------"
    pushd "$d/.." > /dev/null
    git "$@"
    popd > /dev/null
done
