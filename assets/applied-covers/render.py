"""
render.py -- render build/<key>.html to build/png/<key>.png at exact print pixels.

Chromium (Playwright) at device scale 1: one CSS px = one print pixel at 300dpi.
Requires Liberation Serif and DejaVu Serif Condensed (fonts-liberation, fonts-dejavu-extra);
it stops if they're missing rather than silently substituting.

Usage: python3 render.py [key ...]
"""
import json, os, subprocess, sys
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(BASE, "build")

def check_fonts():
    out = subprocess.run(["fc-list"], capture_output=True, text=True).stdout
    spine_font = json.load(open(os.path.join(BASE, "calibration.json")))["spine"].get("font_family", "DejaVu Serif")
    missing = [f for f in ("Liberation Serif", spine_font) if f not in out]
    if missing:
        sys.exit("Missing fonts: " + ", ".join(missing) + " -- install them before rendering.")

def main(keys):
    check_fonts()
    manifest = json.load(open(os.path.join(BUILD, "manifest.json")))
    os.makedirs(os.path.join(BUILD, "png"), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        for m in manifest:
            if keys and m["key"] not in keys:
                continue
            pg = b.new_page(viewport={"width": m["full_px"], "height": m["fullh_px"]}, device_scale_factor=1)
            pg.goto("file://" + m["html"])
            pg.evaluate("document.fonts.ready")
            pg.wait_for_load_state("networkidle")
            out = os.path.join(BUILD, "png", m["key"] + ".png")
            pg.screenshot(path=out, full_page=False)
            pg.close()
            print("rendered", os.path.relpath(out, BASE))
        b.close()

if __name__ == "__main__":
    main(sys.argv[1:])
