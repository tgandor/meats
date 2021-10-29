#!/usr/bin/env python

"""
Create a document with rendered citations.
"""

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("bib_database")
parser.add_argument("bib_style")
parser.add_argument("cite_keys", nargs="+")
parser.add_argument("--output", "-o", default="citations")
args = parser.parse_args()

template = r"""\documentclass[a4paper, 12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[none]{hyphenat}

\title{Citations}
\author{tgandor}

\begin{document}

\maketitle

\section{Enumerating the citations}

\begin{itemize}
%s
\end{itemize}


\bibliographystyle{%s}
\bibliography{%s}

\end{document}
"""

citations = "\n".join(
    f"\\item {key} " r"\cite{" f"{key}" "}" for key in args.cite_keys
)

data = template % (citations, args.bib_style, args.bib_database)

with open(f"{args.output}.tex", "w") as f:
    f.write(data)

# yes, it seems this needs to be 4 passes ;)
os.system(f"pdflatex {args.output}.tex")
os.system(f"bibtex {args.output}.aux")
os.system(f"pdflatex {args.output}.tex")
os.system(f"pdflatex {args.output}.tex")
os.system(f"xdg-open {args.output}.pdf")
