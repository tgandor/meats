#!/bin/bash

if [ -z "$1" ] ; then
	echo "Usage: $0 file.pdf"
	exit
fi

cp "$1" /tmp/tonumber.pdf

cat >/tmp/tonum.tex <<EOF
\documentclass[8pt]{book}
\usepackage[final]{pdfpages}
\usepackage{fancyhdr}

\topmargin 70pt
\oddsidemargin 150pt
\evensidemargin -40pt

\pagestyle{fancy}
\fancyhead{}
\fancyfoot{}
\fancyfoot[LE,RO]{\Large\thepage}

\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\begin{document}
\includepdfset{pages=-,pagecommand=\thispagestyle{fancy}}
\includepdf{tonumber.pdf}
\end{document}
EOF

pushd /tmp
pdflatex tonum.tex
popd

cp /tmp/tonum.pdf "num_$1"
rm /tmp/tonum*
