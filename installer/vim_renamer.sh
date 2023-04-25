#!/bin/bash

pathogen=~/.vim/autoload/pathogen.vim 
mkdir -p ~/.vim/autoload ~/.vim/bundle
[ -f $pathogen ] && echo "$pathogen present already" || curl -LSso $pathogen https://tpo.pe/pathogen.vim
cd ~/.vim/bundle
[ -d vim-renamer ] && echo "vim-renamer already in ~/.vim/bundle" || git clone https://github.com/qpkorr/vim-renamer.git
grep pathogen ~/.vimrc && echo "Pathogen already in .vimrc" || ( echo "execute pathogen#infect()" >> ~/.vimrc )

