#!/usr/bin/env python
"""rename_invoice.py — rename Polish invoice PDFs with payment date and amount prefix.

Usage: rename_invoice.py [-n] file [file ...]

Renames each PDF file to:
    YYYY-MM-DD-NNN,GG-<original_name>.pdf

where YYYY-MM-DD is the payment deadline (Termin płatności) and NNN,GG is the
amount to pay (Do zapłaty) in Polish złote/grosze notation.

Already-renamed files (name already starts with YYYY-MM-DD-) are skipped.
Text extraction uses pypdf layout mode, same as pdfgrep.py.
"""

import argparse
import glob
import re
import shutil
import sys
from pathlib import Path

from pypdf import PdfReader

# ── regex patterns ────────────────────────────────────────────────────────────
# Payment deadline — various spellings/layouts
_DATE_RE = re.compile(
    r"Termin\s+p[łlø]atno[śs]ci\s*:?\s*"
    r"(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{4}"  # dd/mm/yyyy
    r"|\d{4}[/\-\.]\d{1,2}[/\-\.]\d{1,2})",  # yyyy-mm-dd
    re.IGNORECASE,
)

# Amount to pay — "Do zapłaty: 4 825,14 zł" (thousands may be separated by space)
_AMOUNT_RE = re.compile(
    r"Do\s+zap[łlø]aty\s*:?\s*([\d][\d\s]*[,\.]\d{2})\s*z?[łl]?",
    re.IGNORECASE,
)

# Guard against re-renaming — already renamed files start with YYYY-MM-DD-
_ALREADY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


# ── helpers ───────────────────────────────────────────────────────────────────


def extract_text(pdf_path: str) -> str:
    """Return full text of PDF extracted in layout mode."""
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"rename_invoice: {pdf_path}: {e}", file=sys.stderr)
        return ""
    parts = []
    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout") or ""
        parts.append(text)
    return "\n".join(parts)


def parse_date(raw: str) -> str | None:
    """Convert dd/mm/yyyy (or yyyy-mm-dd variants) to YYYY-MM-DD."""
    raw = raw.strip()
    m = re.match(r"^(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})$", raw)
    if m:
        d, mo, y = m.groups()
        return f"{y}-{mo.zfill(2)}-{d.zfill(2)}"
    m = re.match(r"^(\d{4})[/\-\.](\d{1,2})[/\-\.](\d{1,2})$", raw)
    if m:
        y, mo, d = m.groups()
        return f"{y}-{mo.zfill(2)}-{d.zfill(2)}"
    return None


def parse_amount(raw: str) -> str | None:
    """Normalise an extracted amount string to Polish 'NNN,GG' notation."""
    # Remove whitespace used as thousands separator
    normalised = re.sub(r"\s+", "", raw.strip())
    # Normalise decimal separator to comma
    normalised = normalised.replace(".", ",")
    if re.match(r"^\d+,\d{2}$", normalised):
        return normalised
    return None


# ── core logic ────────────────────────────────────────────────────────────────


def process_pdf(pdf_path: Path, dry_run: bool = False, keep: bool = False) -> bool:
    name = pdf_path.name

    if _ALREADY_RE.match(name):
        print(f"skip (already renamed): {name}")
        return True

    text = extract_text(str(pdf_path))
    if not text:
        return False

    # Payment date
    m = _DATE_RE.search(text)
    if not m:
        print(
            f"rename_invoice: {name}: payment date (Termin płatności) not found",
            file=sys.stderr,
        )
        if dry_run:
            pdf_path.with_suffix(".txt").write_text(text)
        return False
    date_iso = parse_date(m.group(1))
    if not date_iso:
        print(
            f"rename_invoice: {name}: cannot parse date {m.group(1)!r}", file=sys.stderr
        )
        return False

    # Amount to pay — take first match (covers single- and multi-invoice PDFs)
    m = _AMOUNT_RE.search(text)
    if not m:
        print(f"rename_invoice: {name}: amount (Do zapłaty) not found", file=sys.stderr)
        return False
    amount = parse_amount(m.group(1))
    if not amount:
        print(
            f"rename_invoice: {name}: cannot parse amount {m.group(1)!r}",
            file=sys.stderr,
        )
        return False

    new_name = f"{date_iso}-{amount}-{name}"
    new_path = pdf_path.parent / new_name

    if new_path.exists():
        print(
            f"rename_invoice: {name}: target already exists: {new_name}",
            file=sys.stderr,
        )
        return False

    if dry_run:
        prefix = "[dry-run] "
    elif keep:
        prefix = "[copy] "
    else:
        prefix = ""
    print(f"{prefix}{name}  →  {new_name}")

    if not dry_run:
        if keep:
            shutil.copy2(pdf_path, new_path)
        else:
            pdf_path.rename(new_path)

    return True


# ── CLI ───────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename Polish invoice PDFs with payment-date and amount prefix",
    )
    parser.add_argument(
        "files", nargs="+", metavar="file", help="PDF file(s) to rename"
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be renamed without touching the files",
    )
    parser.add_argument(
        "-k",
        "--keep",
        action="store_true",
        help="Copy the file instead of renaming it (original is preserved)",
    )
    args = parser.parse_args()

    # Expand globs (useful on Windows where the shell doesn't expand them)
    paths: list[Path] = []
    for f in args.files:
        if any(c in f for c in "*?["):
            expanded = glob.glob(f)
            if not expanded:
                print(f"rename_invoice: {f}: no match", file=sys.stderr)
            paths.extend(Path(p) for p in sorted(expanded))
        else:
            paths.append(Path(f))

    errors = 0
    for path in paths:
        if not path.exists():
            print(f"rename_invoice: {path}: not found", file=sys.stderr)
            errors += 1
            continue
        if path.suffix.lower() != ".pdf":
            print(f"rename_invoice: {path}: not a PDF file", file=sys.stderr)
            errors += 1
            continue
        if not process_pdf(path, dry_run=args.dry_run, keep=args.keep):
            errors += 1

    sys.exit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
