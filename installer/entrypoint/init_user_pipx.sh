#!/bin/bash

python3 -m venv poet
source poet/bin/activate
pip install pipx
pipx install poetry
pipx install pipx
pipx ensurepath

if [ ! -f $HOME/.gitconfig ] ; then
    echo "BTW, initializing $HOME/.gitconfig"
    cp $(dirname "$0")/../configs/gitconfig $HOME/.gitconfig
fi
