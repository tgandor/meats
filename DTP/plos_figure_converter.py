#!/usr/bin/env python

import argparse
import os
import pathlib
import re
import subprocess
import sys

graphics = re.compile(r"\\includegraphics([^{]*)\{([a-zA-Z0-9_/.]+)\}")
tikz_on = r"\begin{tikzpicture}"
tikz_off = r"\end{tikzpicture}"


def convert(in_file, out_eps):
    print(f"Converting {in_file} to {out_eps}...", file=sys.stderr)
    # I wanted to give subprocess a chance...
    if in_file.endswith(".pdf"):
        # subprocess.call('pdftops -eps', in_file, out_eps)
        os.system(f"pdftops -eps {in_file} {out_eps}")
    elif in_file.endswith(".png"):
        # subprocess.call('convert -format eps', in_file, out_eps)
        os.system(f"convert -format eps {in_file} {out_eps}")


def _parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument(
        "--no-include", "-n", action="store_true", help="no includegraphics in output"
    )
    parser.add_argument(
        "--no-convert", "-f", action="store_true", help="no mogrify/pdftops to FigN.eps"
    )
    parser.add_argument(
        "--tikz", "-t", action="store_true", help="replace/remove TikZ drawings"
    )
    return parser.parse_args()


class Processor:
    def __init__(
        self, input: pathlib.Path, no_convert=False, no_include=True, tikz=False
    ) -> None:
        self.fig = 0
        self.tikz_fig = -1  # tikz `external' figures go from zero
        self.in_tikz = False
        self.input = input
        self.no_convert = no_convert
        self.no_include = no_include
        self.tikz = tikz

    @property
    def out_eps(self):
        """The current figure to convert to."""
        return f"Fig{self.fig}.eps"

    def _output_graphics(self, line):
        if self.no_include:
            # commenting out works!
            line = "%" + line
        sys.stdout.write(line)

    def _convert(self, source):
        if self.no_convert:
            return
        convert(source, self.out_eps)

    def process_line(self, line):
        if line.strip() == tikz_on:
            self.in_tikz = True

        if self.in_tikz and line.strip() == tikz_off:
            self.fig += 1
            self.tikz_fig += 1
            self.in_tikz = False
            if self.tikz:
                ext_tikz = f"{self.input.stem}-figure{self.tikz_fig}.pdf"
                self._convert(ext_tikz)
                line = "    \\includegraphics[width=\\textwidth]{}\n".format(
                    "{" + self.out_eps + "}"
                )
                return self._output_graphics(line)

        if self.tikz and self.in_tikz:
            # at the start or inside TikZ
            return

        if m := graphics.match(line.strip()):
            self.fig += 1
            # print(fig, line, m.groups())
            _, graphic = m.groups()
            self._convert(graphic)
            line = line.replace(graphic, self.out_eps)
            return self._output_graphics(line)

        sys.stdout.write(line)

    def process(self):
        if self.tikz:
            subprocess.Popen(
                f"pdflatex -shell-escape {self.input}",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).wait()

        with self.input.open() as fs:
            while line := fs.readline():
                self.process_line(line)


def main():
    args = _parse_cli()
    processor = Processor(**vars(args))
    processor.process()


if __name__ == "__main__":
    main()
