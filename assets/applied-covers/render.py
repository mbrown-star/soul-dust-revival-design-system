"""
render.py -- render build/<key>.html to build/png/<key>.png at exact print pixels.

Chromium (Playwright) at device scale 1: one CSS px = one print pixel at 300dpi.
Requires Liberation Serif and DejaVu Serif Condensed, bundled in fonts/ and installed automatically;
it stops if they're missing rather than silently substituting. It also stops if the hero photo
(hero-source.png) is missing or doesn't load, instead of rendering a cover with no photo.

Usage: python3 render.py [key ...]
"""
import json, os, re, shutil, subprocess, sys
from playwright.sync_api import sync_playwright

from guards import GuardError, build_dir

BASE = os.path.dirname(os.path.abspath(__file__))
BUILD = build_dir(BASE)

def install_bundled_fonts():
    """Copy fonts/ into ~/.fonts and refresh the cache, so any machine renders identically."""
    src = os.path.join(BASE, "fonts")
    if not os.path.isdir(src):
        return
    # ~/.fonts is what fontconfig (Linux Chromium) reads; macOS Chromium only sees ~/Library/Fonts.
    dsts = [os.path.expanduser("~/.fonts")]
    if sys.platform == "darwin":
        dsts.append(os.path.expanduser("~/Library/Fonts"))
    for dst in dsts:
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src):
            if f.endswith(".ttf") and not os.path.exists(os.path.join(dst, f)):
                shutil.copy(os.path.join(src, f), dst)
    subprocess.run(["fc-cache", "-f"], capture_output=True)

def check_fonts():
    install_bundled_fonts()
    out = subprocess.run(["fc-list"], capture_output=True, text=True).stdout
    spine_font = json.load(open(os.path.join(BASE, "calibration.json")))["spine"].get("font_family", "DejaVu Serif")
    missing = [f for f in ("Liberation Serif", spine_font) if f not in out]
    if missing:
        sys.exit("Missing fonts: " + ", ".join(missing) + " -- install them before rendering.")

def hero_path(html_file):
    """The hero photo the generated HTML points at; stop if it isn't there."""
    src = open(html_file, encoding="utf-8").read()
    mo = re.search(r'<div class="photo">.*?<img src="file://([^"]+)"', src, re.S)
    if not mo:
        raise GuardError(f"{html_file} has no hero photo <img>; re-run gen_covers.py")
    path = mo.group(1)
    if not os.path.isfile(path):
        raise GuardError(f"hero photo not found at {path}. Put hero-source.png beside the scripts "
                         "(zip) or one folder up (design system), re-run gen_covers.py, then render.")
    return path


def main(keys):
    check_fonts()
    manifest = json.load(open(os.path.join(BUILD, "manifest.json")))
    os.makedirs(os.path.join(BUILD, "png"), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        for m in manifest:
            if keys and m["key"] not in keys:
                continue
            hero_path(m["html"])
            pg = b.new_page(viewport={"width": m["full_px"], "height": m["fullh_px"]}, device_scale_factor=1)
            pg.goto("file://" + m["html"])
            pg.evaluate("document.fonts.ready")
            pg.wait_for_load_state("networkidle")
            if not pg.evaluate("(() => { const i = document.querySelector('.photo img');"
                               " return !!i && i.complete && i.naturalWidth > 0; })()"):
                b.close()
                raise GuardError(f"[{m['key']}] the hero photo did not load in Chromium; nothing rendered")
            out = os.path.join(BUILD, "png", m["key"] + ".png")
            pg.screenshot(path=out, full_page=False)
            pg.close()
            print("rendered", os.path.relpath(out, BASE))
        b.close()

if __name__ == "__main__":
    main(sys.argv[1:])
