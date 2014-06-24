#!/bin/bash
if [ ! -f menu.txt ] ; then
	echo "Missing menu.txt"
	exit
fi

prices=`perl -ne 'print "$1\n" if /\(([\d\.]+) zł\)/;' menu.txt | sort -n | uniq`
echo $prices
echo ./rucksack.py $1 $2 ...
./rucksack.py $1 $2 $prices | sort -n > results.txt
vi +`wc -l results.txt`

