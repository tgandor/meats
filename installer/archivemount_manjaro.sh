#!/bin/bash

# Alternative to:
# git clone https://github.com/cybernoid/archivemount
# cd archivemount
# autoreconf -i
# ./configure && make && sudo make install

pamac build archivemount-git
