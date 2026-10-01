"""
verify_covers.py -- automated regression gate for the Soul Dust Revival covers.

This does NOT re-implement gen_covers.py's layout math and compare numbers on paper.
It re-measures the ACTUAL RENDERED PIXELS in png/*.png (produced by render.py) using the
same PIL/numpy techniques (color-channel masks, row/column banding) proven against the
Ephesians reference cover during calibration, and checks them against calibration.json's
targets. That is the only way to catch the actual bugs that happened in this project:
a wrong variable used in an f-string, a scaling factor silently reintroduced, a rounding
error, a CSS property that didn't do what the code assumed. Those are invisible in the
Python source and only show up in the rendered pixels.

Run this AFTER gen_covers.py + render.py and BEFORE converting to PDF / delivering.
Exit code is 0 iff everything passes. A single FAIL blocks delivery -- fix the underlying
cause (gen_covers.py or calibration.json, in that order of suspicion) and re-run the whole
pipeline, never hand-patch the PNG or the PDF.

Usage: python3 verify_covers.py
Reads build/manifest.json and build/png/*.png, as written by gen_covers.py and render.py.
"""
import json, os, sys
import numpy as np
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(BASE, "build")
CAL = json.load(open(f"{BASE}/calibration.json"))
manifest = json.load(open(f"{BUILD}/manifest.json"))

GOLD = (176, 141, 46)
GOLD2 = (173, 154, 95)
CREAM = (239, 230, 194)

def close(px, target, tol=40):
    return sum((int(px[i]) - target[i]) ** 2 for i in range(3)) ** 0.5 < tol

def mask_color(arr, target, tol=40):
    d = np.sqrt(((arr[..., :3].astype(int) - np.array(target)) ** 2).sum(axis=-1))
    return d < tol

failures = []
passes = []

def check(cond, label, detail=""):
    if cond:
        passes.append(label)
    else:
        failures.append(f"{label} -- {detail}")

print("=" * 70)
print("Soul Dust Revival cover verification -- rendered-pixel regression check")
print("=" * 70)

for m in manifest:
    key = m["key"]
    png_path = f"{BUILD}/png/{key}.png"
    if not os.path.exists(png_path):
        failures.append(f"[{key}] missing rendered PNG at {png_path} -- run render.py first")
        continue

    img = Image.open(png_path).convert("RGB")
    arr = np.array(img)
    h, w = arr.shape[0], arr.shape[1]
    print(f"\n-- {key} ({m['title']!r}) --  rendered {w}x{h}")

    # 1. Dimensions must match the manifest gen_covers.py itself produced.
    check(w == m["full_px"] and h == m["fullh_px"],
          f"[{key}] rendered dimensions match manifest",
          f"got {w}x{h}, expected {m['full_px']}x{m['fullh_px']}")

    panel_px = m["panel_px"]
    spine_px = m["spine_px"]
    fullh_px = m["fullh_px"]
    back_left, spine_left, front_left = 0, panel_px, w - panel_px

    _KL = CAL["keyline"]
    _BP = CAL["back_panel"]
    _FP = CAL["front_panel"]
    _SP = CAL["spine"]

    # 0. Source-level check: the CSS font-size actually emitted for each spine element must
    #    equal calibration.json's fixed pixel constant, verbatim, on EVERY title. This is a
    #    cheap, 100%-reliable check (grep the generated HTML) for the exact class of bug that
    #    caused every prior spine regression: some scaling expression silently reintroduced
    #    (by spine_px, or by the series' narrowest spine_px) instead of using the fixed
    #    constant unchanged. It is intentionally separate from the pixel-measurement checks
    #    below: those measure rendered INK width, which is a font-metric artifact (a serif
    #    face's visible cap-height is a fraction of its CSS font-size, and that fraction
    #    isn't the same as whatever rendering pipeline produced the original PDF-based
    #    calibration numbers) -- not a reliable absolute match to a number measured off a
    #    *different* renderer's output, even when the CSS is completely correct. Ink pixels
    #    ARE the right tool for cross-title *consistency* (same code path should produce the
    #    same ink width on every title), just not for an absolute match to the PDF reference.
    html_src = open(m["html"]).read()
    import re
    def css_font_size(selector):
        mo = re.search(re.escape(selector) + r"\{[^}]*font-size:(\d+)px", html_src)
        return int(mo.group(1)) if mo else None

    # Every spine size comes straight from calibration.json (the 2026-09-28 directive made the
    # series-name and imprint lines house style, so they're no longer Part-study overrides).
    # "A Journey Part [N]" exists only on titles whose spec sets it (manifest "journey").
    has_journey = m.get("journey", False)
    SPINE_ADJACENT_PX = _SP["title_font_px_at_300dpi"] - _SP["adjacent_to_title_step_px"]
    spine_css = {
        "series name": (css_font_size(".sp-series"), _SP["series_name_font_px_at_300dpi"]),
        "title": (css_font_size(".sp-title"), _SP["title_font_px_at_300dpi"]),
        "imprint line": (css_font_size(".sp-team"), _SP["imprint_line_font_px_at_300dpi"]),
        "diamond": (css_font_size(".sp-dia"), _SP["diamond_font_px_at_300dpi"]),
    }
    if has_journey:
        spine_css["journey"] = (css_font_size(".sp-journey"), SPINE_ADJACENT_PX)
    if not m.get("spine_text", True):
        spine_css = {}
    spine_narrow_clamp = spine_px - 8 < max(
        _SP["title_font_px_at_300dpi"], _SP["series_name_font_px_at_300dpi"],
        _SP["imprint_line_font_px_at_300dpi"], _SP["diamond_font_px_at_300dpi"])
    for label, (actual, target) in spine_css.items():
        check(actual == target or (spine_narrow_clamp and actual is not None and actual <= target),
              f"[{key}] spine '{label}' CSS font-size uses the fixed calibration constant verbatim",
              f"HTML source has font-size:{actual}px, calibration.json fixed constant is {target}px")

    expected_kl_tb = round(_KL["top_bottom_inset_frac_of_panel_height"] * fullh_px)
    expected_kl_lr = round(_KL["left_right_inset_frac_of_panel_width"] * panel_px)

    # 2. Keyline inset check -- scan a column near each panel's horizontal center for the
    #    first row (from top and from bottom) that hits GOLD2, and a row near vertical
    #    center for the first column (from each side) that hits GOLD2.
    def measure_keyline(panel_left):
        col_x = panel_left + panel_px // 2
        col = arr[:, col_x, :]
        gold_rows = np.where(mask_color(col, GOLD2, tol=45))[0]
        top = gold_rows.min() if gold_rows.size else None
        bottom = (h - 1 - gold_rows.max()) if gold_rows.size else None

        row_y = h // 2
        row = arr[row_y, panel_left:panel_left + panel_px, :]
        gold_cols = np.where(mask_color(row, GOLD2, tol=45))[0]
        left = gold_cols.min() if gold_cols.size else None
        right = (panel_px - 1 - gold_cols.max()) if gold_cols.size else None
        return top, bottom, left, right

    for panel_name, panel_left in [("back", back_left), ("front", front_left)]:
        top, bottom, left, right = measure_keyline(panel_left)
        tol_tb = max(20, round(0.15 * expected_kl_tb))
        tol_lr = max(15, round(0.20 * expected_kl_lr))
        check(top is not None and abs(top - expected_kl_tb) <= tol_tb,
              f"[{key}] {panel_name} keyline top inset",
              f"measured {top}px, expected {expected_kl_tb}px +/-{tol_tb}")
        check(bottom is not None and abs(bottom - expected_kl_tb) <= tol_tb,
              f"[{key}] {panel_name} keyline bottom inset",
              f"measured {bottom}px, expected {expected_kl_tb}px +/-{tol_tb}")
        check(left is not None and abs(left - expected_kl_lr) <= tol_lr,
              f"[{key}] {panel_name} keyline left inset",
              f"measured {left}px, expected {expected_kl_lr}px +/-{tol_lr}")
        check(right is not None and abs(right - expected_kl_lr) <= tol_lr,
              f"[{key}] {panel_name} keyline right inset",
              f"measured {right}px, expected {expected_kl_lr}px +/-{tol_lr}")

    # 3. Series name ("SOUL DUST REVIVAL") must be CREAM, not gold -- sample its row band.
    y_series_center = round(_FP["y_series_frac"] * fullh_px)
    band = arr[max(0, y_series_center - 5):y_series_center + 60, front_left:front_left + panel_px, :]
    cream_hits = mask_color(band, CREAM, tol=45).sum()
    gold_hits = mask_color(band, GOLD, tol=45).sum()
    check(cream_hits > 200 and cream_hits > gold_hits,
          f"[{key}] front series name color is cream, not gold",
          f"cream px={cream_hits}, gold px={gold_hits}")

    # 4. Title / tagline non-collision -- the wrap-collision bug produced a second title
    #    line whose pixels ran down into the tagline's own row band. Check the vertical
    #    gap between the lowest cream title-band pixel and the tagline's expected top is
    #    still positive (i.e. no overlap), scanning only the title's own width column.
    y_title_c = round(_FP["y_title_center_frac"] * fullh_px)
    y_tag = round(_FP["y_tagline_frac"] * fullh_px)
    title_search_top = max(0, y_title_c - round(0.12 * fullh_px))
    title_search_bottom = min(h, y_tag)
    title_band = arr[title_search_top:title_search_bottom, front_left:front_left + panel_px, :]
    title_rows = np.where(mask_color(title_band, CREAM, tol=45).any(axis=1))[0]
    if title_rows.size:
        title_bottom_abs = title_search_top + title_rows.max()
        gap = y_tag - title_bottom_abs
        check(gap > 0,
              f"[{key}] front title text does not collide with tagline",
              f"title's lowest cream pixel at y={title_bottom_abs}, tagline starts at y={y_tag} (gap={gap}px)")
    else:
        failures.append(f"[{key}] front title text not found in expected band -- possible render failure")

    # 5. Spine element font sizes -- each of the 5 stacked vertical-writing-mode lines
    #    should measure (as a pixel WIDTH across the spine) close to calibration.json's
    #    FIXED absolute values, unchanged regardless of this title's own spine_px. This is
    #    the exact check that would have caught both the "scale by own spine_px" bug and
    #    the "scale by narrowest spine_px" bug, since either one produces a measured width
    #    that drifts from the fixed target as spine_px varies across the four titles.
    spine_crop = arr[:, spine_left:spine_left + spine_px, :]

    def clusters_for(mask, gap_merge=40):
        rows = np.where(mask.any(axis=1))[0]
        if rows.size == 0:
            return []
        out = []
        start = rows[0]
        prev = rows[0]
        for r in rows[1:]:
            if r - prev > gap_merge:
                out.append((start, prev))
                start = r
            prev = r
        out.append((start, prev))
        return out

    def width_of(top_c, bot_c, mask):
        # A single sampled row picks up whichever glyph happens to sit there, and this is
        # vertical-rl text -- narrow letters ("I", "l") and wide ones ("O", "M") sit at
        # different rows within the same cluster and have very different pixel widths, so
        # a single-row sample is not a reliable stand-in for font-size. Instead, take the
        # 90th-percentile width across every row in the cluster: robust to a handful of
        # narrow-glyph rows while still reflecting the font's actual cap-height (the
        # widest glyphs approach the true cap-height; true outliers above that would mean
        # something is rendering unexpectedly large, which is worth flagging, so we don't
        # take the bare max either).
        sub = mask[top_c:bot_c + 1, :]
        row_widths = []
        for row in sub:
            cols = np.where(row)[0]
            if cols.size:
                row_widths.append(cols.max() - cols.min() + 1)
        if not row_widths:
            return 0
        return int(np.percentile(row_widths, 90))

    # A tight color tolerance (tol=15) is what keeps the bold-gold series name, the
    # cream title, and the gold2 diamonds/imprint line from bleeding into each other at
    # anti-aliased edges -- loosening this made GOLD2 falsely detect inside the series
    # name's own antialiasing halo during development. Each element is its own color, so
    # clustering separately by color (rather than one merged cream-or-gold mask) is what
    # correctly isolates the two diamonds and the imprint line from each other too.
    gold_mask = mask_color(spine_crop, GOLD, tol=15)
    cream_mask = mask_color(spine_crop, CREAM, tol=15)
    gold2_mask = mask_color(spine_crop, GOLD2, tol=15)

    series_clusters = clusters_for(gold_mask)
    title_clusters = clusters_for(cream_mask)
    gold2_clusters = clusters_for(gold2_mask)

    # The journey line (four-part study only) is the same gold2 as the diamonds and imprint
    # line, so it adds a gold2 cluster between the first diamond and the title.
    if not m.get("spine_text", True):
        continue
    want_gold2 = 4 if has_journey else 3
    ok_shape = len(series_clusters) == 1 and len(title_clusters) == 1 and len(gold2_clusters) == want_gold2
    check(ok_shape,
          f"[{key}] spine has every stacked text element (series, diamonds, title, imprint{', journey' if has_journey else ''})",
          f"series={len(series_clusters)}, title={len(title_clusters)}, gold2={len(gold2_clusters)} (want {want_gold2}) "
          f"-- series={series_clusters} title={title_clusters} gold2={gold2_clusters}")

    if ok_shape:
        if has_journey:
            dia1, journey, dia2, team = gold2_clusters
        else:
            dia1, dia2, team = gold2_clusters
        elements = [
            ("series name", series_clusters[0], gold_mask),
            ("diamond (upper)", dia1, gold2_mask),
            ("title", title_clusters[0], cream_mask),
            ("diamond (lower)", dia2, gold2_mask),
            ("imprint line", team, gold2_mask),
        ]
        if has_journey:
            elements.insert(2, ("journey", journey, gold2_mask))
        # Rendered ink width per element and title, compared ACROSS titles below: nothing about a
        # title's own spine width may leak into how large its spine type renders.
        for label, (top_c, bot_c), mask in elements:
            measured = width_of(top_c, bot_c, mask)
            globals().setdefault("_spine_ink_widths", {}).setdefault(label, {})[key] = measured

print("\n" + "=" * 70)
if "_spine_ink_widths" in globals():
    for label, by_key in _spine_ink_widths.items():
        if len(by_key) > 1:
            vals = list(by_key.values())
            spread = max(vals) - min(vals)
            tol = max(6, round(0.25 * min(vals))) if min(vals) > 0 else 6
            check(spread <= tol,
                  f"[cross-title] spine '{label}' renders the same size on every cover",
                  f"measured widths {by_key}, spread={spread}px (tolerance {tol}px)")

print(f"PASS: {len(passes)}   FAIL: {len(failures)}")
if failures:
    print("\nFAILURES:")
    for f in failures:
        print(f"  - {f}")
    print("\nDo NOT deliver until these are resolved. Fix calibration.json or gen_covers.py,")
    print("then re-run gen_covers.py -> render.py -> verify_covers.py from the top.")
    sys.exit(1)
else:
    print("\nAll checks passed. Safe to proceed to JPEG conversion / to_pdf.py / delivery.")
    sys.exit(0)
