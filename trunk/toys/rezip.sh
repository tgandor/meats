#!/bin/bash

unzip $1 -d _recompress_temp
cd _recompress_temp
zip -9 -r ../_recompress_temp.zip *
cd ..
rm -r _recompress_temp
mv $1 $1.bak
mv _recompress_temp.zip $1

