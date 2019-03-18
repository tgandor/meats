#!/bin/bash 

function q {
    exit
}

function hello {
    echo Hello!
}

function eh {
    echo $1
}

function nop {
    return
# you won't see this either:
    echo Nope
}

hello
eh world
nop
q

# hint: this won't happen:
echo foo
