import argparse

import win32clipboard as cb
import win32con


def build_cf_html(html_fragment: str) -> str:
    """
    Build a CF_HTML payload according to the specification:
    https://learn.microsoft.com/windows/win32/dataxchg/html-clipboard-format
    """
    # Minimal valid document containing StartFragment/EndFragment markers
    prefix = (
        "Version:0.9\r\n"
        "StartHTML:{st_html:010d}\r\n"
        "EndHTML:{end_html:010d}\r\n"
        "StartFragment:{st_frag:010d}\r\n"
        "EndFragment:{end_frag:010d}\r\n"
    )
    # Wrap the fragment in a body and include the comment markers required by the spec
    pre = "<html><body><!--StartFragment-->"
    post = "<!--EndFragment--></body></html>"
    full = pre + html_fragment + post

    # First calculate the numeric offsets, then insert them into the header
    # We count bytes in UTF-8 (Office accepts this), but the string put on the clipboard
    # is a Python str (effectively UTF-8/Unicode). In practice this works for ASCII/UTF-8.
    # If using non-ASCII characters test carefully or prefer ASCII in link/text.
    header_placeholder = prefix.format(st_html=0, end_html=0, st_frag=0, end_frag=0)
    start_html = len(header_placeholder)
    start_frag = start_html + len(pre)
    end_frag = start_frag + len(html_fragment)
    end_html = start_html + len(full)

    header = prefix.format(
        st_html=start_html, end_html=end_html, st_frag=start_frag, end_frag=end_frag
    )
    return header + full


def copy_rich_url_to_clipboard(url: str, display_text: str):
    html_a = f'<a href="{url}">{display_text}</a>'
    cf_html = build_cf_html(html_a)

    cb.OpenClipboard()
    try:
        cb.EmptyClipboard()

        # Register the HTML clipboard format if necessary
        cf_format = cb.RegisterClipboardFormat("HTML Format")

        # Set plain text (fallback)
        cb.SetClipboardData(win32con.CF_UNICODETEXT, display_text)

        # Set HTML
        # In pywin32, data for custom clipboard formats must be passed as bytes.
        cb.SetClipboardData(cf_format, cf_html.encode("utf-8"))
    finally:
        cb.CloseClipboard()


def handle_url(url: str, display_text: str | None):
    if display_text is None:
        display_text = url.split("/")[-1] or url
    copy_rich_url_to_clipboard(url=url, display_text=display_text)
    print(f"Copied to clipboard: [{display_text}]({url})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy an HTML hyperlink with a text fallback to the Windows clipboard."
    )
    parser.add_argument(
        "url", help="URL to copy as an HTML hyperlink, or '-' to read from stdin"
    )
    parser.add_argument("display_text", help="Text to display as a fallback", nargs="?")
    args = parser.parse_args()

    if args.url == "-":
        try:
            while True:
                line = input()
                if not line:
                    break
                handle_url(url=line, display_text=None)
        except EOFError:
            pass
        exit(0)

    handle_url(url=args.url, display_text=args.display_text)
