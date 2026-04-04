#!/usr/bin/env python
"""rename_invoice.py — rename Polish invoice PDFs/images with payment date and amount prefix.

Usage: rename_invoice.py [-n] [-k] file [file ...]

Renames each file to:
    YYYY-MM-DD-NNN,GG-<original_name>.ext

where YYYY-MM-DD is the payment deadline (Termin płatności) and NNN,GG is the
amount to pay (Do zapłaty) in Polish złote/grosze notation.

Supported input formats:
  PDF  — text extracted via pypdf layout mode
  JPEG/PNG/TIFF/BMP — OCR via pytesseract (requires Tesseract + Polish pack)

Already-renamed files (name already starts with YYYY-MM-DD-) are skipped.
"""

import argparse
import glob
import re
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
import pytesseract
from pypdf import PdfReader

_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"}
_PDF_SUFFIX = ".pdf"

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


def extract_text_pdf(pdf_path: str) -> str:
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


def _preprocess_for_ocr(img: np.ndarray) -> np.ndarray:
    """Convert image to a clean binary image suitable for Tesseract."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    # Adaptive threshold handles uneven lighting (e.g. phone photos)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
    )
    return binary


def extract_text_image(image_path: str) -> str:
    """Return OCR text from an image using Tesseract (Polish language)."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise OSError("cv2.imread returned None")
    except Exception as e:
        print(f"rename_invoice: {image_path}: {e}", file=sys.stderr)
        return ""
    processed = _preprocess_for_ocr(img)
    try:
        text = pytesseract.image_to_string(processed, lang="pol+eng")
    except pytesseract.TesseractNotFoundError:
        print(
            "rename_invoice: Tesseract not found. Install it and add to PATH.",
            file=sys.stderr,
        )
        sys.exit(2)
    except Exception as e:
        print(f"rename_invoice: {image_path}: OCR error: {e}", file=sys.stderr)
        return ""
    return text


def extract_text(file_path: str) -> str:
    """Dispatch to PDF or image extractor based on file extension."""
    suffix = Path(file_path).suffix.lower()
    if suffix == _PDF_SUFFIX:
        return extract_text_pdf(file_path)
    if suffix in _IMAGE_SUFFIXES:
        return extract_text_image(file_path)
    return ""


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
        if path.suffix.lower() not in {_PDF_SUFFIX} | _IMAGE_SUFFIXES:
            print(
                f"rename_invoice: {path}: unsupported file type "
                f"(supported: pdf, jpg, png, tiff, bmp)",
                file=sys.stderr,
            )
            errors += 1
            continue
        if not process_pdf(path, dry_run=args.dry_run, keep=args.keep):
            errors += 1

    sys.exit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
