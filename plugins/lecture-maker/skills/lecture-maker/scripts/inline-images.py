#!/usr/bin/env python3
"""
Fold every local image in a deck into the HTML file itself, so the deck stays
one file.

Build the deck with ordinary paths while you work:

    <img src="img/dartmouth.jpg" alt="">

then run this once at the end:

    python3 inline-images.py deck.html                 # rewrites deck.html
    python3 inline-images.py deck.html --out final.html
    python3 inline-images.py deck.html --max-width 1600 --quality 78

Every <img src="…">, every srcset entry and every url(…) in a style attribute
that points at a file on disk is resized, re-encoded and replaced with a data
URI. Images that are already data URIs, or that live at a http(s) address, are
left alone. A remote address in a finished deck is a bug: the deck must open
with no internet.

Pillow does the resizing when it is installed. Without it the file is embedded
at its original size, which still works but makes a heavier deck.
"""

import argparse, base64, io, mimetypes, os, re, sys

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

PAT = re.compile(r'(?:src|href)\s*=\s*"([^"]+)"|url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)')
SKIP = ("data:", "http://", "https://", "#", "mailto:")
RASTER = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff"}


def encode(path, max_width, quality):
    ext = os.path.splitext(path)[1].lower()
    raw = open(path, "rb").read()
    before = len(raw)

    if HAVE_PIL and ext in RASTER and ext != ".gif":
        im = Image.open(io.BytesIO(raw))
        if im.width > max_width:
            im = im.resize((max_width, round(im.height * max_width / im.width)),
                           Image.LANCZOS)
        buf = io.BytesIO()
        if im.mode in ("RGBA", "LA", "P") and ext == ".png":
            im.convert("RGBA").save(buf, "PNG", optimize=True)
            mime = "image/png"
        else:
            im.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True,
                                   progressive=True)
            mime = "image/jpeg"
        out = buf.getvalue()
        if len(out) < before or im.width < Image.open(io.BytesIO(raw)).width:
            raw = out
        else:
            mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    else:
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"

    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode()), before, len(raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--out")
    ap.add_argument("--max-width", type=int, default=1600,
                    help="a 1280 wide board never needs more than this")
    ap.add_argument("--quality", type=int, default=78)
    a = ap.parse_args()

    html = open(a.deck, encoding="utf-8").read()
    root = os.path.dirname(os.path.abspath(a.deck))
    done, saved, missing = {}, 0, []

    def swap(m):
        nonlocal saved
        ref = m.group(1) or m.group(2)
        if not ref or ref.startswith(SKIP):
            return m.group(0)
        path = ref if os.path.isabs(ref) else os.path.join(root, ref)
        if not os.path.isfile(path):
            missing.append(ref)
            return m.group(0)
        if ref not in done:
            uri, before, after = encode(path, a.max_width, a.quality)
            done[ref] = uri
            saved += before - after
            print("  %-42s %7.0f KB -> %6.0f KB" % (ref, before / 1024, after / 1024))
        return m.group(0).replace(ref, done[ref])

    out_html = PAT.sub(swap, html)
    out_path = a.out or a.deck
    open(out_path, "w", encoding="utf-8").write(out_html)

    print("\n  %d image(s) inlined, %.0f KB saved by resizing" % (len(done), saved / 1024))
    print("  %s is now %.1f MB" % (out_path, len(out_html.encode()) / 1048576))
    if not HAVE_PIL:
        print("  Pillow is not installed, so nothing was resized. pip install pillow")
    if missing:
        print("  NOT FOUND, still pointing at a file that is not there:")
        for r in dict.fromkeys(missing):
            print("    " + r)
        sys.exit(1)
    if len(out_html.encode()) > 15 * 1048576:
        print("  Over 15 MB. The pictures are too large, not too many.")


if __name__ == "__main__":
    main()
