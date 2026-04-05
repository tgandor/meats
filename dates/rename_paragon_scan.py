#!/usr/bin/env python
"""rename_paragon_scan.py — OCR-based renamer for scanned receipts / simplified invoices.

Usage: rename_paragon_scan.py [-n] [-i] [-d] file [file ...]

Renames each image to:
    YYYY-MM-DD-NNN,GG-<original_name>.ext

Handles:
  • Paragony z NIP nabywcy (faktury uproszczone, ≤450 PLN)
  • Faktury gotówkowe / sprzedaży
  • Partially truncated scans (e.g. "UMA PLN", "026-04-05")
  • Multiple amounts on one line (netto/VAT/brutto — takes largest)
  • Amount on next line after keyword

Supported input: JPEG, PNG, TIFF, BMP
"""

import argparse
import glob
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import pytesseract

# ── constants ─────────────────────────────────────────────────────────────────
_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"}
_ALREADY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
# Raw pattern fragment used in multiple places
_AMT_PAT = r"\d[\d\s]*,\d{2}"
_AMT_RE = re.compile(_AMT_PAT)


# ── data model ────────────────────────────────────────────────────────────────

@dataclass
class Candidate:
    value: str      # normalised: ISO date "YYYY-MM-DD" or amount "NNN,GG"
    raw: str        # original matched text
    context: str    # surrounding lines for display
    priority: int   # 1–5, higher = more reliable
    source: str     # pattern name


# ── text extraction ───────────────────────────────────────────────────────────

def _preprocess(img: np.ndarray) -> np.ndarray:
    """Grayscale + adaptive threshold. Upscale small images for better OCR."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    h, w = gray.shape[:2]
    # Upscale if image is small (receipts are often narrow phone shots)
    if max(h, w) < 1200:
        scale = 1200 / max(h, w)
        gray = cv2.resize(gray, None, fx=scale, fy=scale,
                          interpolation=cv2.INTER_CUBIC)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
    )
    return binary


def extract_text(image_path: str) -> str:
    """OCR an image file using Tesseract with Polish language pack."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise OSError("cv2.imread returned None")
    except Exception as e:
        print(f"rename_paragon_scan: {image_path}: {e}", file=sys.stderr)
        return ""
    processed = _preprocess(img)
    try:
        # PSM 6 = assume uniform text block; config for better digit/comma accuracy
        cfg = r"--psm 6 -c tessedit_char_whitelist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzĄąĆćĘęŁłŃńÓóŚśŹźŻżàáâãäÀÁÂÃÄ0123456789 :,./-'"
        text = pytesseract.image_to_string(processed, lang="pol+eng", config=cfg)
    except pytesseract.TesseractNotFoundError:
        print(
            "rename_paragon_scan: Tesseract not found — install it and add to PATH.\n"
            "  Windows: https://github.com/UB-Mannheim/tesseract/wiki",
            file=sys.stderr,
        )
        sys.exit(2)
    except Exception as e:
        print(f"rename_paragon_scan: {image_path}: OCR error: {e}", file=sys.stderr)
        return ""
    return text


# ── parsing helpers ───────────────────────────────────────────────────────────

def _get_context(text: str, start: int, end: int, lines: int = 2) -> str:
    """Surrounding lines with the matched span highlighted."""
    all_lines = text.splitlines()
    # Find which line numbers the span straddles
    pos = 0
    line_starts = []
    for l in all_lines:
        line_starts.append(pos)
        pos += len(l) + 1  # +1 for \n

    def line_of(char_pos: int) -> int:
        for i, ls in enumerate(line_starts):
            if i + 1 < len(line_starts) and line_starts[i + 1] > char_pos:
                return i
        return len(all_lines) - 1

    lo = max(0, line_of(start) - lines)
    hi = min(len(all_lines) - 1, line_of(max(start, end - 1)) + lines)
    matched_range = set(range(line_of(start), line_of(max(start, end - 1)) + 1))
    result = []
    for i in range(lo, hi + 1):
        prefix = ">>> " if i in matched_range else "    "
        result.append(f"{prefix}{all_lines[i]}")
    return "\n".join(result)


def parse_date(raw: str) -> Optional[str]:
    """Normalise various date formats to YYYY-MM-DD."""
    raw = raw.strip()
    # YYYY-MM-DD or YYYY/MM/DD or YYYY.MM.DD
    m = re.match(r"^(\d{4})[-/\.](\d{1,2})[-/\.](\d{1,2})", raw)
    if m:
        y, mo, d = m.groups()
        return f"{y}-{mo.zfill(2)}-{d.zfill(2)}"
    # dd.mm.yyyy / dd/mm/yyyy / dd-mm-yyyy
    m = re.match(r"^(\d{1,2})[-/\.](\d{1,2})[-/\.](\d{4})", raw)
    if m:
        d, mo, y = m.groups()
        return f"{y}-{mo.zfill(2)}-{d.zfill(2)}"
    # Truncated year: 0YY-MM-DD → 20YY-MM-DD
    m = re.match(r"^(0\d{2})[-/\.](\d{2})[-/\.](\d{2})", raw)
    if m:
        y_trunc, mo, d = m.groups()
        return f"2{y_trunc}-{mo}-{d}"
    return None


def parse_amount(raw: str) -> Optional[str]:
    """Normalise amount string to 'NNN,GG'."""
    # Strip spaces / dots used as thousands separators (before comma)
    norm = re.sub(r"[\s\.](?=\d{3}(?:,|$|\s))", "", raw.strip())
    norm = norm.replace(".", ",")
    if re.match(r"^\d+,\d{2}$", norm):
        return norm
    return None


def _largest_amount(raws: list[str]) -> Optional[str]:
    """Return the raw amount string with the highest numeric value."""
    def to_float(r: str) -> float:
        p = parse_amount(r)
        return float(p.replace(",", ".")) if p else -1.0
    valid = [r for r in raws if parse_amount(r)]
    return max(valid, key=to_float) if valid else None


# ── candidate extraction ──────────────────────────────────────────────────────

def find_dates(text: str) -> list[Candidate]:
    """Return all date candidates with priority scores."""
    candidates: list[Candidate] = []
    seen_values: set[str] = set()

    _DATE_BODY = (
        r"(\d{4}[-/\.]\d{2}[-/\.]\d{2}(?:\s+\d{2}:\d{2}(?::\d{2})?)?"
        r"|\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4})"
    )

    labeled = [
        ("data_wystawienia", 5,
         re.compile(r"Data\s+wystawienia\s*:?\s*" + _DATE_BODY, re.I)),
        ("data_sprzedazy", 5,
         re.compile(r"Data\s+sprzeda[żz]y\s*:?\s*" + _DATE_BODY, re.I)),
        ("data_transakcji", 4,
         re.compile(r"Data\s+(?:transakcji|wydruku|paragonu)\s*:?\s*" + _DATE_BODY, re.I)),
        ("data_zakupu", 4,
         re.compile(r"Data\s+zakupu\s*:?\s*" + _DATE_BODY, re.I)),
    ]
    for source, prio, pat in labeled:
        for m in pat.finditer(text):
            parsed = parse_date(m.group(1))
            if parsed and parsed not in seen_values:
                seen_values.add(parsed)
                candidates.append(Candidate(
                    value=parsed, raw=m.group(1),
                    context=_get_context(text, m.start(), m.end()),
                    priority=prio, source=source,
                ))

    # Partial label — truncated scan (e.g. "ata wystawienia" — leading D cut off)
    partial_label = re.compile(
        r"D?ata\s+wystawienia\s*:?\s*" + _DATE_BODY, re.I
    )
    for m in partial_label.finditer(text):
        raw = m.group(1)
        # Try to repair 3-digit truncated year (026-04-05 → 2026-04-05)
        raw_fixed = re.sub(r"^(0\d{2})([-/\.])", r"2\1\2", raw)
        parsed = parse_date(raw_fixed)
        if parsed and parsed not in seen_values:
            seen_values.add(parsed)
            candidates.append(Candidate(
                value=parsed, raw=raw,
                context=_get_context(text, m.start(), m.end()),
                priority=4, source="partial_label",
            ))

    # Standalone ISO date YYYY-MM-DD
    iso_re = re.compile(
        r"(?<!\d)(\d{4}[-/]\d{2}[-/]\d{2})(?:\s+\d{2}:\d{2}(?::\d{2})?)?(?!\d)"
    )
    for m in iso_re.finditer(text):
        parsed = parse_date(m.group(1))
        if parsed and parsed not in seen_values:
            seen_values.add(parsed)
            candidates.append(Candidate(
                value=parsed, raw=m.group(1),
                context=_get_context(text, m.start(), m.end()),
                priority=3, source="iso_date",
            ))

    # dd.mm.yyyy
    dmy_re = re.compile(r"(?<!\d)(\d{2}\.\d{2}\.\d{4})(?!\d)")
    for m in dmy_re.finditer(text):
        parsed = parse_date(m.group(1))
        if parsed and parsed not in seen_values:
            seen_values.add(parsed)
            candidates.append(Candidate(
                value=parsed, raw=m.group(1),
                context=_get_context(text, m.start(), m.end()),
                priority=2, source="dmy_date",
            ))

    # dd/mm/yyyy
    dmy2_re = re.compile(r"(?<!\d)(\d{2}/\d{2}/\d{4})(?!\d)")
    for m in dmy2_re.finditer(text):
        parsed = parse_date(m.group(1))
        if parsed and parsed not in seen_values:
            seen_values.add(parsed)
            candidates.append(Candidate(
                value=parsed, raw=m.group(1),
                context=_get_context(text, m.start(), m.end()),
                priority=2, source="dmy_slash_date",
            ))

    # Truncated 3-digit year: e.g. 026-04-05 → 2026-04-05
    trunc_re = re.compile(r"(?<!\d)(0\d{2}[-/\.]\d{2}[-/\.]\d{2})(?!\d)")
    for m in trunc_re.finditer(text):
        raw_fixed = "2" + m.group(1)
        parsed = parse_date(raw_fixed)
        if parsed and parsed not in seen_values:
            seen_values.add(parsed)
            candidates.append(Candidate(
                value=parsed, raw=m.group(1),
                context=_get_context(text, m.start(), m.end()),
                priority=1, source="truncated_year",
            ))

    return candidates


def find_amounts(text: str) -> list[Candidate]:
    """Return all amount candidates with priority scores."""
    candidates: list[Candidate] = []
    seen_values: set[str] = set()

    def _add(raw: str, ctx_start: int, ctx_end: int, prio: int, source: str) -> None:
        parsed = parse_amount(raw)
        if parsed and parsed not in seen_values:
            seen_values.add(parsed)
            candidates.append(Candidate(
                value=parsed, raw=raw,
                context=_get_context(text, ctx_start, ctx_end),
                priority=prio, source=source,
            ))

    def _amounts_after(start: int, chars: int = 60) -> list[str]:
        return _AMT_RE.findall(text[start: start + chars])

    # ── Priority 5: SUMA PLN / SUMA: PLN ──
    suma_re = re.compile(
        r"SUMA\s*:?\s*(?:PLN\s*)?(" + _AMT_PAT + r")", re.I
    )
    for m in suma_re.finditer(text):
        _add(m.group(1), m.start(), m.end(), 5, "SUMA")

    # ── Priority 5: Razem do zapłaty ──
    for m in re.finditer(
        r"Razem\s+do\s+zap[łlø]aty\s*:?\s*(?:PLN\s*)?", text, re.I
    ):
        amts = _amounts_after(m.end())
        if amts:
            best = _largest_amount(amts)  # handles netto/vat/brutto trap
            if best:
                _add(best, m.start(), m.end() + 60, 5, "razem_do_zaplaty")

    # ── Priority 4: Zapłacono gotówką / kartą / przelewem ──
    for m in re.finditer(
        r"Zap[łlø]acono\s+(?:got[óo]wk[ąa]|kart[ąa]|przelewem)\s*:?\s*(?:PLN\s*)?",
        text, re.I,
    ):
        amts = _amounts_after(m.end(), 40)
        if amts:
            best = _largest_amount(amts)
            if best:
                _add(best, m.start(), m.end() + 40, 4, "zaplacono")

    # ── Priority 4: Do zapłaty PLN (amount may be on next line) ──
    for m in re.finditer(
        r"Do\s+zap[łlø]aty\s*(?:PLN)?\s*:?\s*", text, re.I
    ):
        amts = _amounts_after(m.end(), 60)
        if amts:
            # Largest handles netto/VAT/brutto trap — brutto is always biggest
            best = _largest_amount(amts)
            if best:
                _add(best, m.start(), m.end() + 60, 4, "do_zaplaty")

    # ── Priority 4: partial SUMA (truncated scan "UMA PLN") ──
    for m in re.finditer(
        r"UMA\s*:?\s*(?:PLN\s*)?(" + _AMT_PAT + r")", text, re.I
    ):
        if not any(c.source == "SUMA" for c in candidates):
            _add(m.group(1), m.start(), m.end(), 4, "partial_SUMA")

    # ── Priority 3: partial "do zapłaty" (e.g. "o zapłaty" — leading D cut off) ──
    for m in re.finditer(
        r"O?\s*zap[łlø]aty\s*(?:PLN)?\s*:?\s*", text, re.I
    ):
        amts = _amounts_after(m.end(), 60)
        if amts:
            best = _largest_amount(amts)
            if best:
                _add(best, m.start(), m.end() + 60, 3, "partial_do_zaplaty")

    # ── Priority 2: largest standalone amount in document ──
    all_amts = _AMT_RE.findall(text)
    if all_amts:
        best_doc = _largest_amount(all_amts)
        if best_doc:
            for m in _AMT_RE.finditer(text):
                if m.group(0) == best_doc:
                    _add(m.group(0), m.start(), m.end(), 2, "largest_in_doc")
                    break

    return candidates


# ── candidate selection ───────────────────────────────────────────────────────

def pick_best(candidates: list[Candidate]) -> Optional[Candidate]:
    """Return highest-priority candidate; ties broken by first occurrence."""
    return max(candidates, key=lambda c: c.priority) if candidates else None


def _dedup(candidates: list[Candidate]) -> list[Candidate]:
    """Keep highest-priority candidate for each distinct value."""
    seen: dict[str, Candidate] = {}
    for c in sorted(candidates, key=lambda c: -c.priority):
        seen.setdefault(c.value, c)
    return sorted(seen.values(), key=lambda c: -c.priority)


def interactive_pick(candidates: list[Candidate], field: str) -> Optional[Candidate]:
    """Display candidates with context, let user choose or enter manually."""
    items = _dedup(candidates)
    if not items:
        print(f"\nBrak kandydatów dla: {field}")
    else:
        print(f"\n{'─'*60}")
        print(f"  Kandydaci — {field}")
        print(f"{'─'*60}")
        for i, c in enumerate(items, 1):
            print(f"\n  [{i}]  value={c.value!r}  prio={c.priority}  źródło={c.source}")
            for line in c.context.splitlines():
                print(f"       {line}")
        print()

    prompt = f"  [1-{len(items)}] wybierz   [0] pomiń   [m] wpisz ręcznie" if items else "  [m] wpisz ręcznie   [0] pomiń"
    print(prompt)
    while True:
        try:
            raw = input(f"  {field} » ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if raw in ("0", ""):
            return None
        if raw == "m":
            val = input(f"  Podaj {field}: ").strip()
            return Candidate(value=val, raw=val, context="", priority=0, source="manual") if val else None
        try:
            idx = int(raw)
            if 1 <= idx <= len(items):
                return items[idx - 1]
        except ValueError:
            pass
        print("  Nieprawidłowy wybór, spróbuj ponownie.")


# ── main file processing ──────────────────────────────────────────────────────

def process_image(
    path: Path,
    *,
    dry_run: bool = False,
    keep: bool = False,
    interactive: bool = False,
    debug: bool = False,
) -> bool:
    name = path.name

    if _ALREADY_RE.match(name):
        print(f"skip (already renamed): {name}")
        return True

    text = extract_text(str(path))
    if not text:
        return False

    if debug:
        print(f"\n{'═'*60}")
        print(f"  OCR text — {name}")
        print(f"{'═'*60}")
        print(text)
        print(f"{'═'*60}\n")

    date_candidates = find_dates(text)
    amount_candidates = find_amounts(text)

    if interactive:
        date_c = interactive_pick(date_candidates, "data wystawienia")
        amount_c = interactive_pick(amount_candidates, "kwota")
    else:
        date_c = pick_best(date_candidates)
        amount_c = pick_best(amount_candidates)

    if not date_c:
        print(f"rename_paragon_scan: {name}: data nie znaleziona", file=sys.stderr)
        if interactive:
            manual = input("  Podaj datę ręcznie (YYYY-MM-DD) lub Enter by pominąć: ").strip()
            if manual and parse_date(manual):
                date_c = Candidate(value=parse_date(manual), raw=manual,
                                   context="", priority=0, source="manual")

    if not amount_c:
        print(f"rename_paragon_scan: {name}: kwota nie znaleziona", file=sys.stderr)
        if interactive:
            manual = input("  Podaj kwotę ręcznie (NNN,GG) lub Enter by pominąć: ").strip()
            if manual and parse_amount(manual):
                amount_c = Candidate(value=parse_amount(manual), raw=manual,
                                     context="", priority=0, source="manual")

    if not date_c or not amount_c:
        return False

    new_name = f"{date_c.value}-{amount_c.value}-{name}"
    new_path = path.parent / new_name

    if new_path.exists():
        print(f"rename_paragon_scan: {name}: cel już istnieje: {new_name}", file=sys.stderr)
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
            shutil.copy2(path, new_path)
        else:
            path.rename(new_path)

    return True


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename scanned receipt / simplified-invoice images with date+amount prefix",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Requires Tesseract with Polish language pack:\n"
            "  Windows: https://github.com/UB-Mannheim/tesseract/wiki\n"
            "  Linux:   sudo apt install tesseract-ocr tesseract-ocr-pol"
        ),
    )
    parser.add_argument("files", nargs="+", metavar="file", help="Image file(s) to process")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Show what would be renamed, make no changes")
    parser.add_argument("-k", "--keep", action="store_true",
                        help="Copy instead of rename (original preserved)")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Show all candidates with context, ask user to confirm")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Print raw OCR text for each file regardless of outcome")
    args = parser.parse_args()

    paths: list[Path] = []
    for f in args.files:
        if any(c in f for c in "*?["):
            expanded = glob.glob(f)
            if not expanded:
                print(f"rename_paragon_scan: {f}: brak plików", file=sys.stderr)
            paths.extend(Path(p) for p in sorted(expanded))
        else:
            paths.append(Path(f))

    errors = 0
    for path in paths:
        if not path.exists():
            print(f"rename_paragon_scan: {path}: plik nie istnieje", file=sys.stderr)
            errors += 1
            continue
        if path.suffix.lower() not in _IMAGE_SUFFIXES:
            print(
                f"rename_paragon_scan: {path}: nieobsługiwany format "
                f"(obsługiwane: jpg, png, tiff, bmp)",
                file=sys.stderr,
            )
            errors += 1
            continue
        if not process_image(
            path,
            dry_run=args.dry_run,
            keep=args.keep,
            interactive=args.interactive,
            debug=args.debug,
        ):
            errors += 1

    sys.exit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
