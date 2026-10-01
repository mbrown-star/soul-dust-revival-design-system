"""
to_pdf.py -- wrap each verified build/png/<key>.png in a single-page, print-ready PDF.

The page is the exact full-wrap size in inches (trim + spine + bleed), with the 300dpi
image placed edge to edge, flattened, as the shipped covers are. Run only after
verify_covers.py exits 0.

Usage: python3 to_pdf.py [key ...]
"""
import json, os, sys
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

BASE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(BASE, "build")

def main(keys):
    manifest = json.load(open(os.path.join(BUILD, "manifest.json")))
    os.makedirs(os.path.join(BUILD, "pdf"), exist_ok=True)
    for m in manifest:
        if keys and m["key"] not in keys:
            continue
        png = os.path.join(BUILD, "png", m["key"] + ".png")
        w_pt, h_pt = m["full_w_in"] * 72, m["full_h_in"] * 72  # exact trim + spine + bleed
        out = os.path.join(BUILD, "pdf", m["file"])
        c = canvas.Canvas(out, pagesize=(w_pt, h_pt))
        c.drawImage(ImageReader(png), 0, 0, width=w_pt, height=h_pt)
        c.showPage(); c.save()
        print(f"wrote {os.path.relpath(out, BASE)}  {m['full_w_in']:.4f}in x {m['full_h_in']:.4f}in")

if __name__ == "__main__":
    main(sys.argv[1:])
