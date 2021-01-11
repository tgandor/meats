#!/bin/bash

sudo apt install -y g++-6 gcc-6

sudo update-alternatives --remove-all gcc
sudo update-alternatives --remove-all g++

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 10
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 20

sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 10
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 20

sudo update-alternatives --install /usr/bin/cc cc /usr/bin/gcc 30
sudo update-alternatives --set cc /usr/bin/gcc

sudo update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++ 30
sudo update-alternatives --set c++ /usr/bin/g++

echo "----------------------------------------------------------------"
echo "Alternatives defined. Running configurations (choose gcc/g++ 6):"
echo "----------------------------------------------------------------"

sudo update-alternatives --config gcc
sudo update-alternatives --config g++
