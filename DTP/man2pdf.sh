#!/bin/bash

for f in /usr/share/man/man*/$1.*.gz ; do
  echo Processing $f
  zcat $f | groff -t -e -mandoc -Tps | ps2pdf14 - `basename $f .gz`.pdf
done

