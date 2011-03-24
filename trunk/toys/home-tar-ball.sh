#! /bin/bash

for f in "$@"; do
  tar xvzf $i
  cd `basename $i .tar.gz`
  ./configure --prefix=$HOME
  make
  make install
  cd ..
done

