#!/bin/bash

shopt -s nullglob

sources=$(echo *.cpp)

if [ -z "$sources" ] ; then
	echo "Error: No *.cpp files found."
	exit
fi

if [ -f CMakeLists.txt ] ; then
	echo "Error: CMakeLists.txt exists. Exiting."
	exit
fi

if [ -z "$1" ] ; then
	project=$(basename "$(pwd)")
else
	project="$1"
fi

echo "project($project)" | tee CMakeLists.txt
echo "cmake_minimum_required(version 2.8)" | tee -a CMakeLists.txt
echo "add_executable($project $sources)" | tee CMakeLists.txt

