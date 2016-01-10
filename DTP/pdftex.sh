#!/bin/sh

pdflatex -output-directory /tmp "$@"
pdflatex -output-directory /tmp "$@"

tex_file=$( (for arg in "$@"; do echo $arg; done) | grep .tex )
pdf_file=/tmp/$(basename $tex_file .tex).pdf

if which okular; then
	okular $pdf_file &
else
	mv -v $pdf_file .
fi
