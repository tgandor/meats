#!/usr/bin/env python3
"""pdftotext replacement using pypdf.

Mimics a subset of poppler's pdftotext options:
  -f <page>   : first page to convert (1-based, default: 1)
  -l <page>   : last page to convert (1-based, default: last)
  -layout     : maintain original physical layout (uses pypdf layout mode)
"""

import argparse
import sys

from pypdf import PdfReader


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file (pypdf-based pdftotext replacement).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("pdf_file", help="PDF file to convert")
    parser.add_argument(
        "output_file",
        nargs="?",
        default="-",
        help="Output text file (default: stdout)",
    )
    parser.add_argument(
        "-f",
        dest="first_page",
        type=int,
        default=1,
        metavar="<int>",
        help="First page to convert (1-based, default: 1)",
    )
    parser.add_argument(
        "-l",
        dest="last_page",
        type=int,
        default=None,
        metavar="<int>",
        help="Last page to convert (1-based, default: last page)",
    )
    parser.add_argument(
        "-layout",
        action="store_true",
        default=False,
        help="Maintain original physical layout",
    )
    args = parser.parse_args()

    extraction_mode = "layout" if args.layout else "plain"

    try:
        reader = PdfReader(args.pdf_file)
    except Exception as e:
        print(f"Error opening '{args.pdf_file}': {e}", file=sys.stderr)
        sys.exit(1)

    total_pages = len(reader.pages)
    first = max(1, args.first_page)
    last = args.last_page if args.last_page is not None else total_pages
    last = min(last, total_pages)

    if first > last:
        print(
            f"Error: first page ({first}) > last page ({last})", file=sys.stderr
        )
        sys.exit(1)

    pages = reader.pages[first - 1 : last]

    out_text = "\f".join(
        page.extract_text(extraction_mode=extraction_mode) or "" for page in pages
    )

    if args.output_file == "-":
        sys.stdout.write(out_text)
        if out_text and not out_text.endswith("\n"):
            sys.stdout.write("\n")
    else:
        try:
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(out_text)
                if out_text and not out_text.endswith("\n"):
                    f.write("\n")
        except OSError as e:
            print(f"Error writing '{args.output_file}': {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
