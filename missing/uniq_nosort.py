#!/usr/bin/env python
"""Remove duplicate lines from a file, preserving the original order."""

import argparse
import sys
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser(
        description="Remove duplicate lines from a file, preserving the original order."
    )
    parser.add_argument("input_file", help="Path to the input file", nargs="?")
    parser.add_argument(
        "--output-file",
        "-o",
        help="Path to the output file. If not provided, print to standard output.",
    )
    parser.add_argument(
        "--count", "-c", action="store_true", help="Count occurrences of each line."
    )
    parser.add_argument(
        "--sort", "-s", action="store_true", help="Sort the output lines (after all)."
    )
    args = parser.parse_args()

    input_path = args.input_file if args.input_file else "input.txt"
    output_path = args.output_file if args.output_file else input_path

    seen = set()
    counts = defaultdict(int)
    unique_lines = []

    if args.input_file is not None and args.input_file != "-":
        with open(input_path, "r", encoding="utf-8") as infile:
            for line in infile:
                if line not in seen:
                    seen.add(line)
                    unique_lines.append(line)
                counts[line] += 1
    else:
        for line in sys.stdin:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
            counts[line] += 1

    if args.sort:
        unique_lines.sort()

    if args.count:
        unique_lines = [f"{counts[line]} {line}" for line in unique_lines]

    if args.output_file is not None:
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.writelines(unique_lines)
    else:
        for line in unique_lines:
            print(line, end="")


if __name__ == "__main__":
    main()
