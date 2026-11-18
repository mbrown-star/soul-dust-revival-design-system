"""
to_pdf.py -- wrap one verified build/png/<key>.png in a single-page, print-ready PDF.

The page is the exact full-wrap size in inches (trim + spine + bleed), with the 300dpi
image placed edge to edge, flattened, as the shipped covers are.

It refuses to export (exit 1, nothing written) unless:
  1. the interior PDF given with --interior has exactly titles/<key>.json's "pages"
     (a stale count gives the wrong spine width: the 2026-10-10 rebuilds);
  2. build/png/<key>.png is newer than build/<key>.html, titles/<key>.json and
     calibration.json (a stale PNG was exported on 2026-10-02);
  3. verify_covers.py passed this exact PNG (build/.verified-<key> holds its SHA-256).

Usage: python3 to_pdf.py <key> --interior <manuscript.pdf>
"""
import argparse
import json
import os
import sys

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from guards import GuardError, build_dir, pdf_page_count, sha256, stamp_path

BASE = os.path.dirname(os.path.abspath(__file__))
BUILD = build_dir(BASE)


def check_interior(key, spec, interior):
    if not os.path.isfile(interior):
        raise GuardError(f"--interior {interior} not found")
    pages = pdf_page_count(interior)
    if pages != spec["pages"]:
        raise GuardError(
            f"[{key}] the interior PDF has {pages} pages but titles/{key}.json says {spec['pages']}. "
            f"The spine would be {spec['pages'] * 0.0025:.4f}in instead of {pages * 0.0025:.4f}in. "
            f"If this is the current interior, set \"pages\": {pages} in titles/{key}.json and rebuild "
            "from gen_covers.py.")
    return pages


def check_fresh(key, png, html):
    sources = [html, os.path.join(BASE, "titles", key + ".json"), os.path.join(BASE, "calibration.json")]
    if not os.path.exists(png):
        raise GuardError(f"[{key}] {png} not found; run render.py and verify_covers.py first")
    newer = [os.path.basename(s) for s in sources
             if os.path.exists(s) and os.path.getmtime(s) > os.path.getmtime(png)]
    if newer:
        raise GuardError(f"[{key}] the rendered PNG is older than {', '.join(newer)}, so it may not show the "
                         "current copy or layout. Re-run gen_covers.py -> render.py -> verify_covers.py.")


def check_stamp(key, png):
    sp = stamp_path(BUILD, key)
    if not os.path.exists(sp):
        raise GuardError(f"[{key}] no verification stamp ({os.path.basename(sp)}); verify_covers.py must "
                         "pass on this PNG first")
    words = open(sp).read().split()
    if not words or words[0] != sha256(png):
        raise GuardError(f"[{key}] the PNG has changed since verify_covers.py passed it; re-run verify_covers.py")


def main(argv):
    ap = argparse.ArgumentParser(description="Export one verified cover PNG to a print PDF.")
    ap.add_argument("key", help="title key, e.g. 1-peter (titles/<key>.json)")
    ap.add_argument("--interior", required=True, metavar="MANUSCRIPT.pdf",
                    help="the current interior PDF; its page count must match the copy file's \"pages\"")
    args = ap.parse_args(argv)
    key = args.key

    spec_path = os.path.join(BASE, "titles", key + ".json")
    if not os.path.exists(spec_path):
        raise GuardError(f"titles/{key}.json not found")
    spec = json.load(open(spec_path))
    manifest = json.load(open(os.path.join(BUILD, "manifest.json")))
    m = next((x for x in manifest if x["key"] == key), None)
    if m is None:
        raise GuardError(f"[{key}] not in build/manifest.json; run gen_covers.py {key} first")

    pages = check_interior(key, spec, args.interior)
    png = os.path.join(BUILD, "png", key + ".png")
    check_fresh(key, png, m["html"])
    check_stamp(key, png)

    os.makedirs(os.path.join(BUILD, "pdf"), exist_ok=True)
    w_pt, h_pt = m["full_w_in"] * 72, m["full_h_in"] * 72  # exact trim + spine + bleed
    out = os.path.join(BUILD, "pdf", m["file"])
    c = canvas.Canvas(out, pagesize=(w_pt, h_pt))
    c.drawImage(ImageReader(png), 0, 0, width=w_pt, height=h_pt)
    c.showPage()
    c.save()
    print(f"wrote {os.path.relpath(out, BASE)}  {m['full_w_in']:.4f}in x {m['full_h_in']:.4f}in "
          f"(interior {pages}pp, spine {m['spine_in']:.4f}in)")


if __name__ == "__main__":
    main(sys.argv[1:])
