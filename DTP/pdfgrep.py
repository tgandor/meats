#!/usr/bin/env python
"""pdfgrep — grep through PDF files via pypdf (layout mode).

Usage: pdfgrep.py [options] PATTERN file [file ...]

Like grep, prefixes matches with 'filename:' when more than one file is given.
Whitespace normalization (collapse runs of spaces, strip leading space) is
opt-in via --strip / -s.
"""

import argparse
import glob
import re
import sys

from pypdf import PdfReader


def extract_lines(pdf_path: str) -> list[str]:
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"pdfgrep: {pdf_path}: {e}", file=sys.stderr)
        return []
    parts = []
    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout") or ""
        parts.append(text)
    return "\f".join(parts).splitlines()


def normalize(line: str) -> str:
    return re.sub(r" +", " ", line).lstrip(" ")


def main():
    parser = argparse.ArgumentParser(
        description="grep through PDFs using pypdf layout extraction",
    )
    parser.add_argument("pattern", help="Regex pattern to search for")
    parser.add_argument("files", nargs="+", metavar="file", help="PDF file(s) to search")
    parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Case-insensitive matching"
    )
    parser.add_argument(
        "-s", "--strip", action="store_true",
        help="Normalize whitespace (collapse spaces, strip leading space)",
    )
    parser.add_argument(
        "-f", "--first-page", type=int, default=1, metavar="N",
        help="First page to search (1-based, default: 1)",
    )
    parser.add_argument(
        "-l", "--last-page", type=int, default=None, metavar="N",
        help="Last page to search (1-based, default: last)",
    )
    args = parser.parse_args()

    flags = re.IGNORECASE if args.ignore_case else 0
    try:
        pattern = re.compile(args.pattern, flags)
    except re.error as e:
        print(f"pdfgrep: invalid pattern: {e}", file=sys.stderr)
        sys.exit(2)

    files: list[str] = []
    for f in args.files:
        if any(c in f for c in "*?"):
            expanded = glob.glob(f)
            if not expanded:
                print(f"pdfgrep: {f}: No match", file=sys.stderr)
            files.extend(sorted(expanded))
        else:
            files.append(f)

    multi = len(files) > 1
    found_any = False

    for pdf_path in files:
        try:
            reader = PdfReader(pdf_path)
        except Exception as e:
            print(f"pdfgrep: {pdf_path}: {e}", file=sys.stderr)
            continue

        total = len(reader.pages)
        first = max(1, args.first_page)
        last = args.last_page if args.last_page is not None else total
        last = min(last, total)

        lines = []
        for page in reader.pages[first - 1 : last]:
            text = page.extract_text(extraction_mode="layout") or ""
            lines.extend(text.splitlines())

        prefix = f"{pdf_path}:" if multi else ""
        for line in lines:
            display = normalize(line) if args.strip else line
            if pattern.search(display):
                print(f"{prefix}{display}")
                found_any = True

    sys.exit(0 if found_any else 1)


if __name__ == "__main__":
    main()
