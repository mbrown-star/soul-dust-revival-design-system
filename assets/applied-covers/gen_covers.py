"""
gen_covers.py -- build the print HTML for Soul Dust Revival wraparound covers.

Reads every layout number from calibration.json (never hardcode one here) and each
title's copy from titles/<key>.json, and writes build/<key>.html plus build/manifest.json.
Then: render.py -> verify_covers.py (must exit 0) -> to_pdf.py.

Usage:
  python3 gen_covers.py                 # every title in titles/
  python3 gen_covers.py ten-commandments 1-peter

Sizes come in two kinds, both from calibration.json:
  - fractions of panel height/width (keyline, padding, the front's main lockup, the
    vertical positions on the front), measured on the Ephesians reference; and
  - fixed pixel sizes at 300dpi (the spine, and the front's secondary lines and the
    whole back panel), identical on every trim. These were measured on the shipped
    6x9 and 8.5x11 covers, which render them at the same pixel size.
"""
import html
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(BASE, "build")
CAL = json.load(open(os.path.join(BASE, "calibration.json")))
DPI = 300
# The hero photo: ../hero-source.png in the design system, or hero-source.png beside this
# script when the pipeline is used on its own (e.g. a Claude Chat project).
HERO = next((p for p in (os.path.join(BASE, "..", "hero-source.png"), os.path.join(BASE, "hero-source.png"))
             if os.path.exists(p)), os.path.join(BASE, "..", "hero-source.png"))
HERO = os.path.abspath(HERO)

GOLD = "#B08D2E"   # back kicker, "EACH WEEK INCLUDES", front theme line, spine series name
GOLD2 = "#AD9A5F"  # keylines, publisher, diamonds, front kicker, tagline, rule, refs, imprint
CREAM = "#EFE6C2"  # titles, series name (front), body copy

# Fonts as rendered in the build container (and as the shipped covers use).
SERIF = '"Liberation Serif", "Times New Roman", serif'        # front and back panels
SPINE_SERIF = '"{}", "DejaVu Serif", serif'.format(CAL["spine"].get("font_family", "DejaVu Serif"))  # spine

TRIMS = {
    # trim: (panel width incl. outer bleed, full height incl. bleed), inches
    "6x9": (6.125, 9.25),
    "8.5x11": (8.625, 11.25),
}
SPINE_IN_PER_PAGE = 0.0025  # cream paper (KDP)
SPINE_TEXT_MIN_PAGES = 79


def esc(s):
    return html.escape(s, quote=True)


def dims(trim, pages):
    panel_in, full_h_in = TRIMS[trim]
    spine_in = pages * SPINE_IN_PER_PAGE
    full_w_in = 2 * panel_in + spine_in
    full_px = round(full_w_in * DPI)
    fullh_px = round(full_h_in * DPI)
    panel_px = round(panel_in * DPI)
    spine_px = full_px - 2 * panel_px
    return dict(panel_in=panel_in, full_w_in=full_w_in, full_h_in=full_h_in, spine_in=spine_in,
                full_px=full_px, fullh_px=fullh_px, panel_px=panel_px, spine_px=spine_px)


def title_px(title, avail_w, fullh):
    """One-line title: capped at the calibrated max, shrunk only as far as needed to fit."""
    fp = CAL["front_panel"]
    fmax = fp["title_font_max_frac_of_panel_height"] * fullh
    fmin = fp["title_min_frac_of_panel_height"] * fullh
    fit = (avail_w * 0.92) / (max(1, len(title)) * 0.52)
    return max(fmin, min(fmax, fit))


def smoothstep_mask(n=10):
    stops = []
    for i in range(n + 1):
        t = i / n
        a = t * t * (3 - 2 * t)
        stops.append(f"rgba(0,0,0,{a:.3f}) {t * 100:.1f}%")
    return ", ".join(stops)


CLOUD_SVG = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E"
             "%3Cfilter id='c'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.014' numOctaves='5' "
             "seed='7' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23c)'/%3E%3C/svg%3E")
GRAIN_SVG = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E"
             "%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' "
             "seed='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23g)'/%3E%3C/svg%3E")


def build(spec):
    d = dims(spec["trim"], spec["pages"])
    W, H, P, S = d["full_px"], d["fullh_px"], d["panel_px"], d["spine_px"]
    kl, bp, fp, sp = CAL["keyline"], CAL["back_panel"], CAL["front_panel"], CAL["spine"]
    fx = CAL["fixed_px_at_300dpi"]
    ground = spec["ground"]
    front, back, spine = spec["front"], spec["back"], spec.get("spine", {})

    kl_tb = round(kl["top_bottom_inset_frac_of_panel_height"] * H)
    kl_lr = round(kl["left_right_inset_frac_of_panel_width"] * P)
    kl_gap = round(kl["double_line_gap_frac_of_panel_height"] * H)
    kl_w = max(1, round(kl["line_weight_frac_of_dpi"] * DPI))
    pad_x = round(bp["content_pad_x_frac_of_panel_width"] * P)
    pad_top = kl_tb + round(bp["content_pad_top_extra_frac_of_panel_height"] * H)
    pad_bottom = kl_tb + round(bp["content_pad_bottom_extra_frac_of_panel_height"] * H)

    # ---- front panel ----
    t_lines = front.get("title_lines") or [front["title"]]
    longest = max(t_lines, key=len)
    t_px = title_px(longest, P - 2 * pad_x, H)
    f = lambda k: fp[k] * H  # noqa: E731
    y = lambda k: round(fp[k] * H)  # noqa: E731

    def line(cls, text, top, extra=""):
        return f'<div class="fl {cls}" style="top:{top}px;{extra}">{text}</div>'

    fr = []
    fr.append(line("f-pub", esc(front.get("publisher", "MARKETLIFE MINISTRIES")), y("y_publisher_frac")))
    fr.append(line("f-series", esc(front.get("series", "SOUL DUST REVIVAL")), y("y_series_frac")))
    fr.append(line("f-dia", "◆ ◆ ◆", y("y_diamonds_frac")))
    if front.get("journey"):
        fr.append(line("f-journey", esc(front["journey"]), round(CAL["series_extras"]["journey_front_y_frac"] * H)))
    if front.get("kicker"):
        fr.append(line("f-kicker", esc(front["kicker"]), y("y_kicker_frac")))
    lh = 1.06
    block_h = t_px * lh * len(t_lines)
    title_top = round(fp["y_title_center_frac"] * H - block_h / 2) if len(t_lines) == 1 else round(fp["y_title_center_frac"] * H - t_px * lh / 2)
    fr.append(f'<div class="fl f-title" style="top:{title_top}px">{"<br>".join(esc(t) for t in t_lines)}</div>')
    shift = round(t_px * lh * (len(t_lines) - 1))  # two-line titles push the stack below down one line
    if front.get("tagline"):
        fr.append(line("f-tag", esc(front["tagline"]), y("y_tagline_frac") + shift))
    fr.append(f'<div class="f-rule" style="top:{y("y_rule_frac") + shift}px"></div>')
    fr.append(line("f-byline", esc(front.get("byline", "The Soul Dust Team")), y("y_byline_frac") + shift))
    anchor = front.get("anchor", ["“My soul clings to the dust;", "Revive me according to Your word.”"])
    fr.append(f'<div class="fl f-anchor" style="top:{y("y_anchor_frac") + shift}px">{"<br>".join(esc(a) for a in anchor)}'
              f'<span class="f-ref">{esc(front.get("anchor_ref", "PSALM 119:25 (NKJV)"))}</span></div>')
    if front.get("theme"):
        fr.append(line("f-theme", esc(front["theme"]), y("y_theme_line_frac")))
    fr.append(line("f-kind", esc(front.get("kind", "A TWELVE-WEEK TOPICAL STUDY")), y("y_kind_line_frac")))

    # ---- back panel ----
    items = "".join(f'<li><span class="b-bul">◆</span>{esc(i)}</li>' for i in back.get("items", []))
    paras = "".join(f'<p class="b-para">{esc(p)}</p>' for p in back.get("paragraphs", []))
    bk = (f'<div class="b-content">'
          f'<div class="b-kicker">{esc(back.get("kicker", front.get("kind", "A TWELVE-WEEK TOPICAL STUDY")))}</div>'
          f'<div class="b-hook">“{esc(back["hook"])}”</div>{paras}'
          f'<div class="b-inc">{esc(back.get("includes_head", "EACH WEEK INCLUDES"))}</div><ul class="b-items">{items}</ul>'
          f'<div class="b-anchor">{esc(back.get("anchor", "“My soul clings to the dust; Revive me according to Your word.”"))}'
          f'<span class="b-ref">{esc(back.get("anchor_ref", "PSALM 119:25 (NKJV)"))}</span></div></div>'
          f'<div class="b-foot"><span class="b-fname">{esc(back.get("footer_name", "The Soul Dust Team"))}</span>'
          f'<span class="b-fsub">{esc(back.get("footer_sub", "MARKETLIFE MINISTRIES · MARKETLIFEMINISTRIES.ORG"))}</span></div>')

    # ---- spine ----
    sp_html = ""
    if spec["pages"] >= SPINE_TEXT_MIN_PAGES:
        parts = [f'<div class="sp sp-series">{esc(spine.get("series", "SOUL DUST REVIVAL"))}</div>',
                 '<div class="sp sp-dia sp-dia1">◆</div>']
        if spine.get("journey"):
            parts.append(f'<div class="sp sp-journey">{esc(spine["journey"])}</div>')
        parts += [f'<div class="sp sp-title">{esc(spine.get("title", t_lines[0]))}</div>',
                  '<div class="sp sp-dia sp-dia2">◆</div>',
                  f'<div class="sp sp-team">{esc(spine.get("team", "THE SOUL DUST TEAM"))}</div>']
        sp_html = "".join(parts)

    def clamp(px):  # only ever shrinks, and only if a spine is narrower than the type
        return min(px, max(8, S - 8))

    gap = lambda k: round(sp[k] * H)  # noqa: E731
    sp_title = clamp(sp["title_font_px_at_300dpi"])
    sp_series = clamp(sp["series_name_font_px_at_300dpi"])
    sp_team = clamp(sp["imprint_line_font_px_at_300dpi"])
    sp_dia = clamp(sp["diamond_font_px_at_300dpi"])
    sp_journey = clamp(sp["title_font_px_at_300dpi"] - sp["adjacent_to_title_step_px"])

    sw = sp.get("font_weights", {"series": "bold", "title": "bold", "imprint": "normal", "journey": "normal"})
    # The photo covers spine + front (cover-fit, centered) and is masked: a smoothstep
    # fade across the spine's own width, fully opaque over the front, nothing on the back.
    ramp = ", ".join(f"rgba(0,0,0,{(i/10)**2*(3-2*i/10):.3f}) {S*i/10:.1f}px" for i in range(11))
    mask = f"linear-gradient(to right, {ramp}, #000 {S}px)"
    css = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{ground}}}
.canvas{{position:relative;width:{W}px;height:{H}px;background:{ground};isolation:isolate;overflow:hidden}}
.cloud{{position:absolute;inset:-25%;background-image:url("{CLOUD_SVG}");background-size:130% 130%;mix-blend-mode:overlay;opacity:{fx["bg_cloud_opacity"]}}}
.photo{{position:absolute;top:0;bottom:0;left:{P}px;right:0;mix-blend-mode:overlay;opacity:{fx["bg_photo_opacity"]};
  -webkit-mask-image:{mask};mask-image:{mask}}}
.photo .tint{{position:absolute;inset:0;isolation:isolate;filter:saturate({fx["bg_photo_saturation"]})}}
.photo img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;filter:grayscale(1)}}
.photo .wash{{position:absolute;inset:0;background:{ground};mix-blend-mode:color}}
.grain{{position:absolute;inset:0;background-image:url("{GRAIN_SVG}");mix-blend-mode:soft-light;opacity:{fx["bg_grain_opacity"]}}}
.glow{{position:absolute;inset:0;background:linear-gradient(to bottom,{fx["bg_glow_color"]} 0%,transparent {fx["bg_glow_extent_pct"]}%)}}
.panel{{position:absolute;top:0;width:{P}px;height:{H}px;font-family:{SERIF};color:{CREAM}}}
.back{{left:0}} .front{{left:{P + S}px}}
.kl{{position:absolute;top:{kl_tb}px;bottom:{kl_tb}px;left:{kl_lr}px;right:{kl_lr}px;border:{kl_w}px solid {GOLD2}}}
.kl::after{{content:"";position:absolute;inset:{kl_gap}px;border:{kl_w}px solid {GOLD2}}}
.fl{{position:absolute;left:0;width:100%;text-align:center;white-space:nowrap}}
.f-pub{{font-size:{f("publisher_line_font_frac_of_panel_height"):.1f}px;font-weight:bold;letter-spacing:.12em;color:{GOLD2}}}
.f-series{{font-size:{f("series_name_font_frac_of_panel_height"):.1f}px;font-weight:bold;letter-spacing:.16em;color:{CREAM}}}
.f-dia{{font-size:{fx["front_diamonds"]}px;letter-spacing:{fx["front_diamonds_letter_spacing_em"]}em;color:{GOLD2};text-indent:{fx["front_diamonds_letter_spacing_em"]}em}}
.f-journey{{font-size:{fx["front_kicker"] * 1.4:.0f}px;font-style:italic;color:{GOLD2}}}
.f-kicker{{font-size:{fx["front_kicker"]}px;font-weight:bold;letter-spacing:.14em;color:{GOLD2}}}
.f-title{{left:50%;transform:translateX(-50%);width:{P - 2 * pad_x}px;font-size:{t_px:.1f}px;line-height:{lh};font-weight:{fp["title_font_weight"]};color:{CREAM}}}
.f-tag{{font-size:{f("tagline_font_frac_of_panel_height"):.1f}px;font-style:italic;color:{GOLD2}}}
.f-rule{{position:absolute;left:50%;transform:translateX(-50%);width:{fx["front_rule_width"]}px;height:{fx["front_rule_thickness"]}px;background:{GOLD2}}}
.f-byline{{font-size:{f("byline_font_frac_of_panel_height"):.1f}px}}
.f-anchor{{left:{pad_x}px;width:{P - 2 * pad_x}px;font-size:{fx["front_anchor"]}px;line-height:{fx["front_anchor_line_height"]};font-style:italic;white-space:normal}}
.f-ref{{display:block;margin-top:{fx["front_ref_gap"]}px;font-style:normal;font-size:{fx["front_ref"]}px;letter-spacing:.08em;color:{GOLD2};line-height:1.2}}
.f-theme{{font-size:{fx["front_theme"]}px;font-weight:bold;letter-spacing:.12em;color:{GOLD}}}
.f-kind{{font-size:{fx["front_kind"]}px;letter-spacing:.1em}}
.b-content{{position:absolute;top:{pad_top}px;left:{pad_x}px;right:{pad_x}px}}
.b-kicker{{font-size:{fx["back_kicker"]}px;font-weight:bold;letter-spacing:.14em;color:{GOLD};line-height:1.2}}
.b-hook{{margin-top:{fx["back_gap_kicker_hook"]}px;font-size:{fx["back_hook"]}px;line-height:{fx["back_hook_line_height"]};font-style:italic}}
.b-para{{margin-top:{fx["back_gap_para"]}px;font-size:{fx["back_body"]}px;line-height:{fx["back_body_line_height"]}}}
.b-inc{{margin-top:{fx["back_gap_inc"]}px;font-size:{fx["back_includes_head"]}px;font-weight:bold;letter-spacing:.08em;color:{GOLD};line-height:1.2}}
.b-items{{list-style:none;margin-top:{fx["back_gap_items"]}px}}
.b-items li{{position:relative;padding-left:{fx["back_item_indent"]}px;font-size:{fx["back_item"]}px;line-height:{fx["back_item_line_height"]};margin-top:{fx["back_item_gap"]}px}}
.b-items li:first-child{{margin-top:0}}
.b-bul{{position:absolute;left:0;top:.15em;font-size:.8em;color:{GOLD2}}}
.b-anchor{{margin-top:{fx["back_gap_anchor"]}px;text-align:center;font-size:{fx["back_anchor"]}px;font-style:italic;line-height:1.3}}
.b-ref{{display:block;margin-top:{fx["back_ref_gap"]}px;font-style:normal;font-weight:bold;font-size:{fx["back_ref"]}px;letter-spacing:.05em;color:{GOLD2};line-height:1.2}}
.b-foot{{position:absolute;left:0;width:100%;bottom:{pad_bottom}px;text-align:center}}
.b-fname{{display:block;font-size:{fx["back_footer_name"]}px;line-height:1.2}}
.b-fsub{{display:block;margin-top:{fx["back_footer_gap"]}px;font-size:{fx["back_footer_sub"]}px;letter-spacing:.08em;color:{GOLD2};line-height:1.2}}
.spine{{position:absolute;top:0;left:{P}px;width:{S}px;height:{H}px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:{SPINE_SERIF}}}
.sp{{writing-mode:vertical-rl;text-orientation:sideways;white-space:nowrap;line-height:1}}
.sp-series{{font-size:{sp_series}px;font-weight:{sw["series"]};letter-spacing:.15em;color:{GOLD}}}
.sp-dia{{font-size:{sp_dia}px;color:{GOLD2}}}
.sp-dia1{{margin-top:{gap("gap_series_to_diamond_frac_of_panel_height")}px}}
.sp-journey{{font-size:{sp_journey}px;font-style:italic;color:{GOLD2};margin-top:{round(CAL["series_extras"]["journey_gap_diamond_frac"] * H)}px}}
.sp-title{{font-size:{sp_title}px;font-weight:{sw["title"]};letter-spacing:.01em;color:{CREAM};margin-top:{gap("gap_diamond_to_title_frac_of_panel_height")}px}}
.sp-dia2{{margin-top:{gap("gap_title_to_diamond_frac_of_panel_height")}px}}
.sp-team{{font-size:{sp_team}px;font-weight:{sw["imprint"]};letter-spacing:.1em;color:{GOLD2};margin-top:{gap("gap_diamond_to_imprint_frac_of_panel_height")}px}}
"""
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{esc(spec["key"])}</title><style>{css}</style></head>
<body><div class="canvas">
<div class="cloud"></div>
<div class="photo"><div class="tint"><img src="file://{HERO}" alt=""><div class="wash"></div></div></div>
<div class="grain"></div>
<div class="glow"></div>
<div class="panel back"><div class="kl"></div>{bk}</div>
<div class="spine">{sp_html}</div>
<div class="panel front"><div class="kl"></div>{"".join(fr)}</div>
</div></body></html>"""
    os.makedirs(BUILD, exist_ok=True)
    out = os.path.join(BUILD, spec["key"] + ".html")
    open(out, "w").write(page)
    return {"key": spec["key"], "title": spec["front"]["title"], "file": spec.get("file", spec["key"] + ".pdf"),
            "html": out, "journey": bool(spine.get("journey")), "spine_text": bool(sp_html), **d}


def main(keys):
    tdir = os.path.join(BASE, "titles")
    names = keys or sorted(f[:-5] for f in os.listdir(tdir) if f.endswith(".json"))
    manifest = []
    for k in names:
        spec = json.load(open(os.path.join(tdir, k + ".json")))
        spec.setdefault("key", k)
        manifest.append(build(spec))
        print(f"built build/{k}.html  {manifest[-1]['full_px']}x{manifest[-1]['fullh_px']}px, spine {manifest[-1]['spine_px']}px")
    os.makedirs(BUILD, exist_ok=True)
    json.dump(manifest, open(os.path.join(BUILD, "manifest.json"), "w"), indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])
