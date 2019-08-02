#!/bin/bash

# this won't help pytorch, if Ubuntu >= 17.10

sudo apt install -y g++-5 gcc-5

set -v

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 10

sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 10

sudo update-alternatives --set gcc /usr/bin/gcc-5

sudo update-alternatives --set g++ /usr/bin/g++-5

update-alternatives --list g++
update-alternatives --list gcc
