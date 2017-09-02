#!/bin/bash

sudo apt-get install vim python3 ruby htop mc python-pip python3-pip python-virtualenv

if [ -n $HOME/.bash_aliases ] ; then
    echo Creating $HOME/.bash_aliases
    tee $HOME/.bash_aliases <<EOF
alias ll='ls -l'
alias la='ls -A'
alias l='ls -CF'
EOF
fi

if [ -n $HOME/.vimrc ] ; then
    echo Creating $HOME/.vimrc
    tee $HOME/.vimrc <<EOF
let _curfile = expand("%:t")
if _curfile =~ "Makefile" || _curfile =~ "makefile" || _curfile =~ ".*\.mk"
	set noexpandtab
else
	set expandtab
	set tabstop=4
	set shiftwidth=4
endif

set laststatus=2
syn on
EOF
fi
