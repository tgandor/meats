#!/bin/bash

sudo apt-get install vim \
    python3 \
    ruby \
    htop \
    mc \
    screen \
	emacs-nox \
    python-pip \
    python3-pip \
    python-virtualenv

if [ ! -e $HOME/.bash_aliases ] ; then
    echo Creating $HOME/.bash_aliases
    tee $HOME/.bash_aliases <<EOF
alias ll='ls -l'
alias la='ls -A'
alias l='ls -CF'
EOF
fi

if [ ! -e $HOME/.vimrc ] ; then
    echo Creating $HOME/.vimrc
    tee $HOME/.vimrc <<EOF
set tabstop=4
set shiftwidth=4
set expandtab

" let _curfile = expand("%:t")
" if _curfile =~ "Makefile" || _curfile =~ "makefile" || _curfile =~ ".*\.mk"
"     set noexpandtab
" else
"     set expandtab
" endif

au FileType make setl noexpandtab

set autoindent
set smartindent
set laststatus=2
syn on
EOF
fi
