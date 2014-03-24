#!/bin/bash
if [ ! -f menu.txt ] ; then
	echo "Missing menu.txt"
	exit
fi

prices=`perl -ne 'print "$1\n" if /\(([\d\.]+) zł\)/;' menu.txt`
echo $prices
./rucksack.py $1 $prices | sort -n > results.txt
vi results.txt +20000

