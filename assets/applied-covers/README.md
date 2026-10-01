# Applied covers: the cover recipe

How to build a Soul Dust Revival wraparound cover. This folder holds the rules (this file), the measured layout numbers (`calibration.json`), the build pipeline (`gen_covers.py`, `render.py`, `verify_covers.py`, `to_pdf.py`), one copy file per title (`titles/`) and the reference cover every title is built to match (`SoulDust_Ephesians_Cover_5_dusk.pdf`). Finished covers are kept in the shared drive under [Claude Code Covers](https://drive.google.com/drive/folders/17VHHakHBc2b0LlbSSa_JYw1e3bshOl4M), not here.

## Trim, classification and spine

- **Book Study** (walks one book cover to cover) is **6x9**. **Topical Study** (a cross-Scripture theme, or a bounded range within a book such as Romans 6–8 or Genesis 1–17) is **8.5x11**. **365-Day Devotional** is **6x9**. When the book-study list and the bounded-range test disagree, the bounded-range test wins.
- **Spine width** = pages × 0.0025in (cream paper, KDP). Recompute it if the paper or binding ever changes.
- **Spine text only at 79+ pages.** Below that, leave the spine blank (texture only).
- **Bleed:** 0.125in on each outer edge. Output is flattened at 300dpi.
- **Barcode zone:** keep the back panel's lower-right 2.1in × 1.35in clear of all text.

## Ground and background

- Each title gets its **own ground color** from `CoverBlendMottlePairings`. Pick one not already in the register below, and choose it from the manuscript's own imagery.
- The mottled ground (flat color + cloud blotch + grain/vignette) runs continuously across back, spine and front.
- The duotone photo blend fades in **only within the spine's width**: transparent at the back/spine line, fully opaque at the spine/front line, eased with smoothstep (`t² × (3 − 2t)`). It never bleeds into the back panel and there's no hard seam.

## Layout (all numbers come from `calibration.json`)

- **Never type a layout number straight into the build script.** If a measurement is in doubt, re-render the reference PDF at 300dpi, re-measure, update `calibration.json`, then rebuild. Measure from the print PDF, never from a screenshot.
- **Keyline:** a gold double line on both front and back. The top/bottom inset is a fraction of panel *height* and the left/right inset a fraction of panel *width* (these are different numbers).
- **Front panel**, top to bottom at fixed fractions of panel height: publisher line, series name (**cream**, not gold), diamond triad, kicker ("A STUDY OF", or "PART [N] · A STUDY OF"), title, italic gold tagline, gold rule, byline ("The Soul Dust Team", title case), Psalm 119:25 (NKJV) anchor verse, gold "FROM DUST TO —" theme line, kind line ("A TWELVE-WEEK TOPICAL STUDY").
- **Title:** set in medium weight (500), not bold. It **must stay on one line**: size it from its character count, capped at the calibrated maximum and scaled down only as far as needed. Titles over ~24 characters (e.g. *Benedictions, Blessings & Doxologies*, *A 365-Day Journey Through the Bible*) take the manuscript title page's own two-line break instead.
- **Tagline:** must also fit on one line, because the rule below it sits at a fixed position. Shorten long manuscript subtitles.
- **Back panel:** kicker, a one-sentence italic hook, two short paragraphs, gold "EACH WEEK INCLUDES" (or "EACH DAY INCLUDES" for the devotional) with diamond bullets, the centered anchor-verse pull-quote and a two-line footer. **Watch the total length:** a long hook, or a normal hook plus two full paragraphs, pushes the pull-quote into the footer, especially on the shorter 6x9 panel. Keep the hook under ~75 characters with no embedded quotation marks.
- **Spine:** each line is its **own** `writing-mode: vertical-rl; text-orientation: sideways` element, stacked in a flex column. Never rotate one assembled block, which puts the lines side by side. Stack: series name / diamond / title / diamond / imprint ("THE SOUL DUST TEAM").
- **Spine type is DejaVu Serif Condensed in fixed pixels at 300dpi:** series name 56px regular, title 54px bold, imprint 54px regular, diamonds 12px (as rendered on every shipped cover since the 2026-09-28 directive). **Never scale them by a title's own spine width, or by the narrowest spine in a series.** Only clamp them down if a spine is ever narrower than 56px. If a spine title is too long to fit, use its first line only (as on the 365-Day Journey).

## Series-specific

The four-part study (*Out of the Dust*, *Formed and Sent*, *Confession & Repentance*, *Life*) adds "A Journey" on the front between the diamonds and the kicker, and "A Journey Part [N]" on the spine between the first diamond and the title. These are constants in the build script only, not in `calibration.json`, and no other title gets them unless asked.

## Building a cover

1. **Write the copy file.** Copy `titles/ten-commandments.json` (8.5x11) or `titles/1-peter.json` (6x9) to `titles/<key>.json` and fill in `trim`, `pages`, `ground` (the hex value from the register or `CoverBlendMottlePairings`), the front lines, the back hook, paragraphs and items, and `file` (the PDF name). Optional: `front.title_lines` for a two-line title, `spine.title` for a shortened spine title, and `front.journey`/`spine.journey` for the four-part study.
2. **Generate:** `python3 gen_covers.py <key>` writes `build/<key>.html` and `build/manifest.json`, reading every size from `calibration.json`.
3. **Render:** `python3 render.py <key>` writes `build/png/<key>.png` at exact print pixels.
4. **Verify:** `python3 verify_covers.py` must exit 0.
5. **Look:** check the full cover and the back, front and spine crops in the PNG, especially back-cover overflow.
6. **Export:** `python3 to_pdf.py <key>` writes `build/pdf/<file>` at the exact full-wrap size. Save it to the title's folder in Claude Code Covers with its build notes, then add the title to the register below and to the changelog.

**Requirements:** Python 3 with `pip install playwright==1.56.0 pillow numpy reportlab` (Playwright uses the installed Chromium), plus the fonts Liberation Serif and DejaVu Serif Condensed (`fonts-liberation` and `fonts-dejavu-extra`). `render.py` stops if a font is missing rather than substituting one. The hero photo is `../hero-source.png`. The `build/` folder is scratch and isn't saved.

**Proven against:** the rebuilt Ten Commandments and 1 Peter covers match the shipped PDFs (mean pixel difference about 4.5/255, text within 0-3px, identical page sizes). The four-part study's "A Journey" lines are supported but haven't been re-checked against those four shipped covers.

## Before delivery

Render → **`verify_covers.py` must exit 0** (it checks keyline insets, title/tagline clearance, spine CSS sizes against `calibration.json`, and that spine type renders the same size on every title) → visually check the full cover plus the back, front and spine crops → convert to PDF → save it to the title's folder in *Claude Code Covers* → add the title to the register below and the changelog.

## Register of shipped covers

| Title | Type | Trim | Pages | Spine | Ground |
|---|---|---|---|---|---|
| 1 Peter | Book Study | 6x9 | 189 | 0.4725in | Soot `#2a2a26` |
| A 365-Day Journey Through the Bible | 365-Day Devotional | 6x9 | 371 | 0.9275in | Slate `#26302f` |
| Benedictions, Blessings & Doxologies: A Scriptural Catalog | Topical Study | 8.5x11 | 14 | blank spine | Navy `#1e2733` |
| Colossians: The All-Sufficient Christ | Book Study | 6x9 | 201 | 0.5025in | Regal `#211b47` |
| Confession & Repentance (Part Three) | Topical Study | 8.5x11 | 127 | 0.3175in | Marrow `#211b16` |
| Dust, Breath, Fall, Promise: A Study in Genesis 1–17 | Topical Study | 8.5x11 | 168 | 0.42in | Peat `#2e2a18` |
| Dusty and Holy: A Twelve-Week Walk Through Hebrews 8–10 | Topical Study | 8.5x11 | 161 | 0.4025in | Veil `#3a1b32` |
| Dusty but Hopeful: A Twelve-Week Walk Through Romans 6–8 | Topical Study | 8.5x11 | 159 | 0.3975in | Tannin `#4a2318` |
| Ecclesiastes: Dust and Vapor | Book Study | 6x9 | 195 | 0.4875in | Umber `#3a281c` |
| Ephesians (reference) | Book Study | 6x9 | — | 0.5625in | Dusk (pairing 01) `#2a4038` |
| Formed and Sent (Part Two) | Topical Study | 8.5x11 | 234 | 0.585in | Iron `#23282b` |
| Galatians: Freed from the Dust by Grace Alone | Book Study | 6x9 | 189 | 0.4725in | Bark `#2e2117` |
| In Christ: The Blessings and Benefits of Being in Christ | Topical Study | 8.5x11 | 128 | 0.32in | Clay `#3a2420` |
| Law and Gospel: The End of Performance, the Riches of Faith | Topical Study | 8.5x11 | 165 | 0.4125in | Stone `#33383a` |
| Life (Part Four) | Topical Study | 8.5x11 | 165 | 0.4125in | Deep-pine `#1f2f2a` |
| Out of the Dust (Part One) | Topical Study | 8.5x11 | 219 | 0.5475in | Soil `#241a12` |
| Philippians: Joy from the Dust in Christ Alone | Book Study | 6x9 | 178 | 0.445in | Char `#1c1611` |
| Prayer | Topical Study | 8.5x11 | 185 | 0.4625in | Smolder `#3d1c0c` |
| Promise, Struggle, Exile, Providence: A Study in Genesis 18–50 | Topical Study | 8.5x11 | 187 | 0.4675in | Basalt `#2a2530` |
| The Gospel | Topical Study | 8.5x11 | 157 | 0.3925in | Garnet `#2e1013` |
| The Holy Spirit | Topical Study | 8.5x11 | 116 | 0.29in | Deep Teal `#12302c` |
| The Sermon on the Mount: Seeing Your Sin, and the Sufficiency of Christ | Topical Study | 8.5x11 | 163 | 0.4075in | Storm `#34383e` |
| The Ten Commandments: Fulfilled and Empowered | Topical Study | 8.5x11 | 183 | 0.4575in | Cinder `#2c211e` |

Ground names follow the 2026-10-01 renames: Soot, Peat, Garnet, Smolder and Tannin were formerly "Ash", "Loam", "Oxblood", "Ember" and "Rust".
