#!/bin/bash

if ! which pipx > /dev/null ; then
    echo "pipx is not installed, starting setup"
    python3 -m venv poet
    source poet/bin/activate
    pip install pipx
    pipx install poetry
    pipx install pipx
    pipx ensurepath
else
    echo "pipx is already installed. (seems)"
fi

if [ ! -f $HOME/.gitconfig ] ; then
    echo "BTW, initializing $HOME/.gitconfig"
    cp $(dirname "$0")/../../configs/gitconfig $HOME/.gitconfig
fi
