#!/bin/bash

g++ -std=c++11 -DSIZE=4 -DVERBOSE=2 wolf_sheep.cpp -o wolf
./wolf
echo "-----------------------------------------"
g++ -std=c++11 -O2 -DSIZE=6 wolf_sheep.cpp -o wolf
./wolf
echo "-----------------------------------------"
g++ -std=c++11 -O2 wolf_sheep.cpp -o wolf
./wolf
