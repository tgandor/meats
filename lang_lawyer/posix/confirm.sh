#!/bin/bash

function confirm(){
    echo '<Enter>, or s to skip, ctrl-c to exit'
    read x || exit
    [ "$x" != "s" ]
}

echo 'Are you sure?'
confirm && echo 'Yes, you were...' || echo 'Skipping.'

