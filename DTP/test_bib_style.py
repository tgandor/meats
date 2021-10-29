#!/usr/bin/env python

# NOTES: maybe get interested in pybtex... Just saying.

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("bib_database")
parser.add_argument("cite_key")
parser.add_argument("bib_style", nargs="+")
args = parser.parse_args()

template = r"""\documentclass[a4paper, 12pt]{article}
\usepackage[utf8]{inputenc}

\title{Citation style preview}
\author{tgandor}

\begin{document}

\maketitle


\section{Citations}

See \cite{%s} (style: %s)


\bibliographystyle{%s}
\bibliography{%s}

\end{document}
"""

for style in args.bib_style:
    data = template % (args.cite_key, style, style, args.bib_database)

    with open(f"cite_{style}.tex", "w") as f:
        f.write(data)

    # yes, it seems this needs to be 4 passes ;)
    os.system(f"pdflatex cite_{style}.tex")
    os.system(f"bibtex cite_{style}.aux")
    os.system(f"pdflatex cite_{style}.tex")
    os.system(f"pdflatex cite_{style}.tex")
    os.system(f"xdg-open cite_{style}.pdf")
