#!/bin/bash

if [ -z "$1" ]; then
	source=fonts_yes.pdf
else
	source="$1"
fi

if [ -z "$2" ]; then
	target=fonts_not.pdf
else
	target="$2"
fi

gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite  -sOutputFile="$target" -dPDFSETTINGS=/default -dEmbedAllFonts=false $source
