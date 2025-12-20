#!/usr/bin/env python3
"""
eml_to_html.py — Convert a .eml email into a viewable HTML file.

Features:
- Prefers text/html part; falls back to text/plain converted to HTML.
- Extracts attachments (including inline images with Content-ID) to a folder and rewrites cid: links.
- Optionally embeds inline attachments as data URIs for a single-file HTML (--embed).
- Adds a small header block with From/To/Subject/Date (can disable with --no-headers).

Usage:
  python eml_to_html.py input.eml [-o output.html] [--outdir assets/] [--embed] [--no-headers]

Notes:
- For multipart/alternative, picks the best representation (HTML > plain).
- For text/plain fallback, preserves formatting and auto-links URLs.
"""

import argparse
import base64
import hashlib
import html
import mimetypes
import os
import re
import sys
from email import policy
from email.parser import BytesParser
from email.message import Message
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, Tuple, Optional

URL_RE = re.compile(
    r'(?P<url>(?:https?|ftp)://[^\s<>"\']+)|(?:www\.[^\s<>"\']+)', re.IGNORECASE
)


def guess_ext(mime: str, filename: Optional[str]) -> str:
    if filename:
        ext = Path(filename).suffix
        if ext:
            return ext
    ext = mimetypes.guess_extension(mime or "")
    return ext or ""


def sanitize_filename(name: str) -> str:
    # Keep it simple and stable
    name = re.sub(r'[\\/:*?"<>|]+', "_", name)
    name = name.strip().strip(".")
    return name or "file"


def best_body(msg: Message) -> Tuple[Optional[bytes], Optional[str], Optional[str]]:
    """
    Returns (payload_bytes, mime_type, charset) for the best body.
    Prefers text/html, then text/plain. If multipart, walks parts.
    """
    if msg.is_multipart():
        # multipart/alternative: prefer HTML over plain
        alts = []
        for part in msg.walk():
            if part.is_multipart():
                continue
            ctype = part.get_content_type()
            if ctype in ("text/html", "text/plain"):
                alts.append((0 if ctype == "text/html" else 1, part))
        if alts:
            alts.sort(key=lambda x: x[0])
            part = alts[0][1]
            ct = part.get_content_type()
            cs = part.get_content_charset() or part.get_param("charset")
            try:
                payload = part.get_payload(decode=True)
            except Exception:
                payload = (part.get_payload() or "").encode(
                    cs or "utf-8", errors="ignore"
                )
            return payload, ct, cs
        # no html/plain? try first text/* we find
        for part in msg.walk():
            if part.is_multipart():
                continue
            if part.get_content_type().startswith("text/"):
                cs = part.get_content_charset() or part.get_param("charset")
                payload = part.get_payload(decode=True)
                return payload, part.get_content_type(), cs
        return None, None, None
    else:
        ctype = msg.get_content_type()
        cs = msg.get_content_charset() or msg.get_param("charset")
        payload = msg.get_payload(decode=True)
        return payload, ctype, cs


def to_html_from_plain(text: str) -> str:
    # Escape HTML
    esc = html.escape(text)
    # Preserve spacing / paragraphs
    esc = esc.replace("\t", "    ")

    # Auto-link URLs
    def repl(m):
        u = m.group("url") or m.group(0)
        url = (
            u
            if u.lower().startswith(("http://", "https://", "ftp://"))
            else f"http://{u}"
        )
        return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(u)}</a>'

    esc = URL_RE.sub(repl, esc)
    # Convert newlines to <br> within paragraphs
    lines = esc.splitlines()
    # Group consecutive non-empty lines into paragraphs
    out = []
    para = []
    for line in lines:
        if line.strip() == "":
            if para:
                out.append("<p>" + "<br>\n".join(para) + "</p>")
                para = []
        else:
            para.append(line)
    if para:
        out.append("<p>" + "<br>\n".join(para) + "</p>")
    return "\n".join(out) if out else "<p></p>"


def collect_inline_parts(msg: Message) -> Dict[str, Tuple[bytes, str, Optional[str]]]:
    """
    Returns a dict mapping Content-ID (without <>) to (data, mime, filename)
    for parts that have Content-ID (typical inline images).
    """
    by_cid = {}
    for part in msg.walk():
        if part.is_multipart():
            continue
        cid = part.get("Content-ID")
        if not cid:
            continue
        cid = cid.strip("<>")
        mime = part.get_content_type()
        fname = part.get_filename()
        try:
            data = part.get_payload(decode=True)
        except Exception:
            data = None
        if data:
            by_cid[cid] = (data, mime, fname)
    return by_cid


def collect_attachments(msg: Message) -> Dict[str, Tuple[bytes, str, Optional[str]]]:
    """
    Attachments without Content-ID (downloadable attachments).
    Returns a dict with stable keys (sha1 prefix) -> (data, mime, filename).
    """
    files = {}
    for part in msg.walk():
        if part.is_multipart():
            continue
        disp = (part.get("Content-Disposition") or "").lower()
        if "attachment" in disp or (part.get_filename() and "inline" not in disp):
            data = part.get_payload(decode=True)
            if not data:
                continue
            mime = part.get_content_type()
            fname = part.get_filename() or f"attachment{guess_ext(mime, None)}"
            sha1 = hashlib.sha1(data).hexdigest()[:12]
            key = f"{sha1}"
            files[key] = (data, mime, fname)
    return files


def embed_data_uri(data: bytes, mime: str) -> str:
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def rewrite_cids(html_src: str, cid_map: Dict[str, str]) -> str:
    # Replace src="cid:..."; also url('cid:...') just in case
    def repl(m):
        cid = m.group(1)
        return f'src="{cid_map.get(cid, m.group(0))}"'

    html_src = re.sub(
        r'src\s*=\s*"cid:([^"]+)"',
        lambda m: f'src="{cid_map.get(m.group(1), m.group(0))}"',
        html_src,
        flags=re.IGNORECASE,
    )
    html_src = re.sub(
        r"url\(\s*['\"]?cid:([^)'\"]+)['\"]?\s*\)",
        lambda m: f"url('{cid_map.get(m.group(1), m.group(0))}')",
        html_src,
        flags=re.IGNORECASE,
    )
    return html_src


def build_header_block(msg: Message) -> str:
    def g(key):
        v = msg.get(key, "")
        return html.escape(v)

    rows = []
    for k in ("From", "To", "Cc", "Subject", "Date"):
        val = g(k)
        if val:
            rows.append(f"<tr><th>{k}</th><td>{val}</td></tr>")
    if not rows:
        return ""
    return f"""
    <table class="meta">
      {''.join(rows)}
    </table>
    """


def wrap_html(doc_body: str, header_html: str, title: str = "Email") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title or 'Email')}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font: 14px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif; color:#222; background:#fff; margin:0; }}
  .container {{ max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
  .meta {{ border-collapse: collapse; margin-bottom: 1rem; }}
  .meta th, .meta td {{ text-align:left; padding: .35rem .6rem; border-bottom: 1px solid #e5e7eb; vertical-align: top; }}
  .meta th {{ width: 7rem; color:#555; font-weight:600; }}
  .content {{ background:#fff; padding:1rem; border:1px solid #e5e7eb; border-radius:8px; }}
  img {{ max-width:100%; height:auto; }}
  blockquote {{ border-left: 4px solid #ddd; margin: .8rem 0; padding: .2rem .8rem; color:#555; }}
  pre, code {{ background:#f6f8fa; border-radius:5px; }}
</style>
</head>
<body>
  <div class="container">
    {header_html}
    <div class="content">
      {doc_body}
    </div>
  </div>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser(
        description="Convert a .eml file into a viewable HTML file."
    )
    ap.add_argument("eml", help="Input .eml path")
    ap.add_argument(
        "-o", "--output", help="Output .html path (default: input.html next to eml)"
    )
    ap.add_argument(
        "--outdir",
        help="Folder to save extracted attachments (default: input_assets)",
        default=None,
    )
    ap.add_argument(
        "--embed",
        action="store_true",
        help="Embed inline attachments (cid:) as data URIs (single-file HTML).",
    )
    ap.add_argument(
        "--no-headers",
        action="store_true",
        help="Do not render From/To/Subject/Date header table.",
    )
    ap.add_argument(
        "--no-date",
        action="store_true",
        help="Do not prefix output with datetime."
    )
    args = ap.parse_args()

    eml_path = Path(args.eml)
    if not eml_path.exists():
        print(f"Input not found: {eml_path}", file=sys.stderr)
        sys.exit(1)

    with eml_path.open("rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # Choose output HTML path
    out_html = Path(args.output) if args.output else eml_path.with_suffix(".html")
    if len(out_html.name.split()) > 1:
        out_html = out_html.with_stem("_".join(out_html.stem.strip().split()))
    if not args.no_date:
        dt = parsedate_to_datetime(msg.get("Date", ""))
        date_str = dt.strftime("%Y%m%d_%H%M") if dt else "nodate"
        out_html = out_html.with_name(f"{date_str}_{out_html.name}")

    # Prepare assets directory if extracting
    if not args.embed:
        if args.outdir:
            assets_dir = Path(args.outdir)
        else:
            assets_dir = out_html.with_suffix("").with_name(out_html.stem + "_assets")
        assets_dir.mkdir(parents=True, exist_ok=True)
    else:
        assets_dir = None

    # Determine body
    body_bytes, mime, charset = best_body(msg)
    body_html = ""
    if body_bytes is None:
        body_html = "<p><em>(No body found)</em></p>"
    else:
        if (mime or "").lower() == "text/html":
            try:
                body_html = body_bytes.decode(charset or "utf-8", errors="replace")
            except LookupError:
                body_html = body_bytes.decode("utf-8", errors="replace")
        else:
            # text/plain or other text/*
            try:
                text = body_bytes.decode(charset or "utf-8", errors="replace")
            except LookupError:
                text = body_bytes.decode("utf-8", errors="replace")
            body_html = to_html_from_plain(text)

    # Inline parts by Content-ID (cid)
    cid_parts = collect_inline_parts(msg)
    cid_map: Dict[str, str] = {}
    for cid, (data, mime_type, fname) in cid_parts.items():
        if args.embed:
            cid_map[cid] = embed_data_uri(data, mime_type)
        else:
            # write to assets dir; choose filename
            base = sanitize_filename(
                fname or f"inline_{cid}{guess_ext(mime_type, fname)}"
            )
            out_path = assets_dir / base
            # avoid overwrite collisions
            i = 1
            while out_path.exists():
                stem = Path(base).stem
                ext = Path(base).suffix
                out_path = assets_dir / f"{stem}_{i}{ext}"
                i += 1
            with out_path.open("wb") as wf:
                wf.write(data)
            cid_map[cid] = str(os.path.relpath(out_path, out_html.parent))

    # Rewrite cid: links in HTML
    if cid_map and body_html:
        body_html = rewrite_cids(body_html, cid_map)

    # Collect regular attachments (non-inline) for listing/download links
    attachments = collect_attachments(msg)
    attach_section = ""
    if attachments:
        links = []
        for key, (data, mime_type, fname) in attachments.items():
            if args.embed:
                # Embed as data URI link for convenience
                uri = embed_data_uri(data, mime_type)
                disp_name = sanitize_filename(
                    fname or f"attachment{guess_ext(mime_type, None)}"
                )
                links.append(
                    f'<li><a href="{uri}" download="{html.escape(disp_name)}">{html.escape(disp_name)}</a> <small>({html.escape(mime_type)})</small></li>'
                )
            else:
                disp_name = sanitize_filename(
                    fname or f"attachment{guess_ext(mime_type, None)}"
                )
                out_path = assets_dir / disp_name
                i = 1
                while out_path.exists():
                    stem = Path(disp_name).stem
                    ext = Path(disp_name).suffix
                    out_path = assets_dir / f"{stem}_{i}{ext}"
                    i += 1
                with out_path.open("wb") as wf:
                    wf.write(data)
                rel = os.path.relpath(out_path, out_html.parent)
                links.append(
                    f'<li><a href="{html.escape(rel)}" download>{html.escape(out_path.name)}</a> <small>({html.escape(mime_type)})</small></li>'
                )
        attach_section = f"""
        <h3>Attachments</h3>
        <ul>
          {''.join(links)}
        </ul>
        """

    header_html = "" if args.no_headers else build_header_block(msg)

    # Final HTML
    full_html = wrap_html(
        doc_body=body_html + attach_section,
        header_html=header_html,
        title=msg.get("Subject", "Email"),
    )

    out_html.parent.mkdir(parents=True, exist_ok=True)
    with out_html.open("w", encoding="utf-8", newline="\n") as wf:
        wf.write(full_html)

    # Print a short summary
    if args.embed:
        print(f"✔ Wrote single-file HTML: {out_html}")
    else:
        print(f"✔ Wrote: {out_html}")
        if attachments or cid_parts:
            print(f"  Assets in: {assets_dir}")


if __name__ == "__main__":
    main()
