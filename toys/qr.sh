#!/bin/bash
qrencode "$1"  -o -| display -resize 300x300% -
