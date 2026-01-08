#!/usr/bin/env python

import argparse
import os


def chunk_csv(input_path, output_dir, chunk_size=1_000_000):
    """
    Split a CSV into chunks with header included in each file.
    :param input_path: Path to the original CSV file
    :param output_dir: Directory to save chunks
    :param chunk_size: Number of data rows per chunk (excluding header)
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as infile:
        header = infile.readline()  # read header line
        chunk_num = 1
        lines = []

        for i, line in enumerate(infile, start=1):
            lines.append(line)
            if i % chunk_size == 0:
                out_path = os.path.join(output_dir, f"chunk_{chunk_num:03}.csv")
                with open(out_path, "w", encoding="utf-8") as outfile:
                    outfile.write(header)
                    outfile.writelines(lines)
                lines.clear()
                chunk_num += 1

        # Write remaining lines
        if lines:
            out_path = os.path.join(output_dir, f"chunk_{chunk_num:03}.csv")
            with open(out_path, "w", encoding="utf-8") as outfile:
                outfile.write(header)
                outfile.writelines(lines)

    print(f"Chunks saved in {output_dir}")


parser = argparse.ArgumentParser(description="Chunk a CSV file into smaller CSV files.")
parser.add_argument("input_csv", help="Path to the input CSV file.")
parser.add_argument(
    "output_dir",
    help="Directory to save the output CSV files. Default: <basename>/.",
    nargs="?",
)
parser.add_argument(
    "--chunk",
    "-c",
    type=int,
    default=10_000_000,
    help="Number of rows per chunk. Default: 10M.",
)
args = parser.parse_args()

input_csv = args.input_csv
output_dir = args.output_dir or os.path.splitext(os.path.basename(input_csv))[0]
chunk_size = args.chunk

chunk_csv(input_csv, output_dir, chunk_size)
