# Applied covers: the cover recipe

How to build a Soul Dust Revival wraparound cover. This folder holds the rules (this file), the measured layout numbers (`calibration.json`), the build pipeline (`gen_covers.py`, `render.py`, `verify_covers.py`, `to_pdf.py`, and `guards.py`, the checks they share), one copy file per title (`titles/`) and the reference cover the layout was measured from (`SoulDust_Ephesians_Cover_5_dusk.pdf`). Finished covers are kept in the shared drive under [Claude Code Covers](https://drive.google.com/drive/folders/17VHHakHBc2b0LlbSSa_JYw1e3bshOl4M), not here. **Those shipped covers are the visual reference: a new cover must look like them.**

## Trim, classification and spine

- **Book Study** (walks one book cover to cover) is **6x9**. **Topical Study** (a cross-Scripture theme, or a bounded range within a book such as Romans 6–8 or Genesis 1–17) is **8.5x11**. **365-Day Devotional** is **6x9**. When the book-study list and the bounded-range test disagree, the bounded-range test wins.
- **Spine width** = pages × 0.0025in (cream paper, KDP). Recompute it if the paper or binding ever changes. **Take the page count from the current interior PDF, never from an old cover's spine width,** and recheck it before each cover export; a stale count makes the spine the wrong width.
- **Spine text only at 79+ pages.** Below that, leave the spine blank (texture only).
- **Bleed:** 0.125in on each outer edge. Output is flattened at 300dpi.
- **Barcode zone:** keep the back panel's lower-right 2.1in × 1.35in clear of all text. Since the **2026-10-02 directive** the back panel has no footer at all, and no back-panel text may sit within 1.6in of the bottom trim. `verify_covers.py` checks this on every build.

## Ground and background

- Each title gets its **own ground color** from `CoverBlendMottlePairings`. Pick one not already in the register below, and choose it from the manuscript's own imagery.
- The background is the one every shipped cover in Claude Code Covers uses: flat ground color, a low-frequency cloud blotch, the hero photo (grayscale, tinted with the ground, desaturated 50%) faded in across the spine, fine grain, and a faint warm glow at the top. All of its settings are in `calibration.json` (`fixed_px_at_300dpi`, `bg_*`).
- The mottled ground runs continuously across back, spine and front.
- The duotone photo blend fades in **only within the spine's width**: transparent at the back/spine line, fully opaque at the spine/front line, eased with smoothstep (`t² × (3 − 2t)`). It never bleeds into the back panel and there's no hard seam.
- This is close to, but not the same as, the swatch recipe on the `CoverBlendMottlePairings` page (the swatches add an edge vignette and a soft highlight, and have no gold glow). The swatches are for choosing a color. **Do not change the background toward the swatch recipe without rebuilding every shipped cover to match**, or new titles will not sit with the series.

## Layout (all numbers come from `calibration.json`)

- **Never type a layout number straight into the build script.** If a measurement is in doubt, re-render the reference PDF at 300dpi, re-measure, update `calibration.json`, then rebuild. Measure from the print PDF, never from a screenshot.
- **Keyline:** a gold double line on both front and back. The top/bottom inset is a fraction of panel *height* and the left/right inset a fraction of panel *width* (these are different numbers). These land at the distances Soul_Dust_Revival_Context.md Section 12E requires (6x9: fore-edge 0.30in, spine side 0.43in, top and bottom 0.475in; 8.5x11: 0.475 / 0.60 / 0.605in).
- **Front panel**, top to bottom at fixed fractions of panel height: publisher line, series name (**cream**, not gold), diamond triad, kicker ("A STUDY OF", or "PART [N] · A STUDY OF"), title, italic gold tagline, gold rule, byline ("The Soul Dust Team", title case), Psalm 119:25 (NKJV) anchor verse, gold "FROM DUST TO —" theme line, kind line ("A TWELVE-WEEK TOPICAL STUDY").
- **Title:** set in medium weight (500), not bold. It **must stay on one line**: size it from its character count, capped at the calibrated maximum and scaled down only as far as needed. Titles over ~24 characters (e.g. *Benedictions, Blessings & Doxologies*, *A 365-Day Journey Through the Bible*) take the manuscript title page's own two-line break instead (`front.title_lines`).
- **Tagline:** must also fit on one line, because the rule below it sits at a fixed position. Shorten long manuscript subtitles.
- **Back panel:** kicker, a one-sentence italic hook, two short paragraphs, gold "EACH WEEK INCLUDES" (or "EACH DAY INCLUDES" for the devotional) with diamond bullets, and the centered anchor-verse pull-quote. **No footer** (2026-10-02 directive, applied to every title). `calibration.json`'s `back_panel.content_pad_bottom_extra_frac_of_panel_height` is 0.12: the blank zone no back text may enter.
- **6x9 back panels** use tighter spacing, from `calibration.json`'s `back_panel_6x9` block (applied automatically by `gen_covers.py` for 6x9 titles only): hook line-height 1.22, body 1.36, items 1.3, large gaps 0.15×DPI, the gap before the bullet list 0.09×DPI. Keep 6x9 copy tight too: a hook under ~75 characters and each paragraph cut to its essential sentence or two. 8.5x11 titles keep the original, more generous spacing.
- **Spine:** each line is its **own** `writing-mode: vertical-rl; text-orientation: sideways` element, stacked in a flex column. Never rotate one assembled block, which puts the lines side by side. Stack: series name / diamond / title / diamond / imprint ("THE SOUL DUST TEAM").
- **Spine type is DejaVu Serif Condensed in fixed pixels at 300dpi:** series name 56px regular, title 54px bold, imprint 54px regular, diamonds 12px. **Never scale them by a title's own spine width, or by the narrowest spine in a series.** Only clamp them down if a spine is ever narrower than 56px. If a spine title is too long to fit, use a shorter form (`spine.title`), as on the 365-Day Journey and the Psalms devotional.

## Series-specific

The four-part study (*Out of the Dust*, *Formed and Sent*, *Confession & Repentance*, *Life*) adds "A Journey" on the front between the diamonds and the kicker, and "A Journey Part [N]" on the spine between the first diamond and the title (`front.journey` / `spine.journey`). No other title gets them unless asked.

## Building a cover

0. **Gather the inputs.** Before starting any cover, make sure you have both the study's manuscript PDF and `SDR-cover-pipeline.zip` (this folder's scripts, fonts and hero photo). Ask for whichever is missing, and don't start without both.
1. **Write the copy file.** Copy `titles/ten-commandments.json` (8.5x11) or `titles/1-peter.json` (6x9) to `titles/<key>.json` and fill in `trim`, `pages`, `ground` (the hex value from the register or `CoverBlendMottlePairings`), the front lines, the back hook, paragraphs and items, and `file` (`Soul_Dust_Revival_<Title_With_Underscores>_Cover.pdf`). Optional: `front.title_lines` for a two-line title, `spine.title` for a shortened spine title, and `front.journey`/`spine.journey` for the four-part study. There is no footer field, and `gen_covers.py` refuses a copy file that has one. `ground` must not already be in the register under another title; `gen_covers.py` refuses that too (titles that share a name, like the four John parts, may share a ground). Every line comes from the manuscript; the store prints the back-cover copy word for word as the title's description.
2. **Generate:** `python3 gen_covers.py <key>` writes `build/<key>.html` and `build/manifest.json`, reading every size from `calibration.json`.
3. **Render:** `python3 render.py <key>` writes `build/png/<key>.png` at exact print pixels. It stops if `hero-source.png` is missing or doesn't load.
4. **Verify:** `python3 verify_covers.py` must exit 0. On a pass it writes `build/.verified-<key>`, the SHA-256 of the PNG it checked.
5. **Look:** check the full cover and the back, front and spine crops in the PNG, especially back-cover overflow, and compare it against a shipped cover of the same trim.
6. **Export:** `python3 to_pdf.py <key> --interior <manuscript.pdf>` writes `build/pdf/<file>` at the exact full-wrap size from the current PNG. `--interior` is required: pass the current interior PDF. It exports one title per run and refuses (exit 1, nothing written) if the interior's page count isn't the copy file's `pages`, if the PNG is older than `build/<key>.html`, `titles/<key>.json` or `calibration.json`, or if there's no verification stamp matching this PNG. Fix the cause and rebuild from step 2; never edit the stamp or touch the PNG to get past it. Open the PDF itself and check it. Save it to the title's folder in Claude Code Covers with its build notes and copy file.

**Requirements:** Python 3 with `pip install playwright==1.56.0 pillow numpy reportlab` (Playwright uses the installed Chromium), plus the fonts Liberation Serif and DejaVu Serif Condensed. Both are bundled in `fonts/`, and `render.py` installs them if they're missing, then stops if they still aren't available rather than substituting. On macOS, `render.py` also copies the fonts into `~/Library/Fonts`, since Chromium there doesn't read `~/.fonts`. The hero photo is `hero-source.png`, beside the scripts in the zip or one folder up (`../hero-source.png`) in the design system; `render.py` stops if it's missing. The `build/` folder is scratch and isn't saved.

**Proven against:** on 2026-11-17 this pipeline rebuilt 1 Peter and Galatians (6x9) and The Ten Commandments and Prayer (8.5x11) from their shipped copy files. Each matched its shipped PDF in Claude Code Covers to within about 4–5/255 mean pixel difference (grain and JPEG noise), with the back-panel text at the identical position. The four-part study's "A Journey" lines are supported but haven't been re-checked against those four shipped covers.

## Before delivery

Render → **`verify_covers.py` must exit 0.** It checks: keyline insets on both panels, the series name is cream, the title doesn't collide with the tagline, spine type sizes match `calibration.json` and render the same size on every title, and no back-panel text sits within 1.6in of the bottom trim (it also prints the blank space below the text as a share of panel height). → Visually check the full cover plus the back, front and spine crops, and compare the blank space with other titles of the same trim. → Export the PDF with `--interior` (it checks the page count against the current interior) and check the PDF itself, not just the PNG. → Save to the title's folder in *Claude Code Covers* (PDF, Build notes.md, the copy file). The daily routine adds the title to the register and changelog.

## Guards and hooks

The checks above that once relied on someone remembering them are now enforced, in two layers:

- **In the scripts** (`guards.py`; they run wherever the pipeline runs, including Cowork and Claude Chat, where Claude Code hooks don't fire): `to_pdf.py` checks the interior page count, a fresh PNG and the verification stamp; `render.py` checks the hero photo; `gen_covers.py` refuses a footer field or a ground another title already uses.
- **Claude Code hooks** (`.claude/settings.json` and `.claude/hooks/` at the design-system repo root; they load when a Claude Code session starts in the repo): after any edit to `gen_covers.py`, `render.py`, `guards.py`, `calibration.json` or `titles/*.json`, the canary titles (1 Peter and The Ten Commandments) and any edited title are rebuilt and verified in a scratch folder, and the edit is flagged to Claude if that fails. After any edit to `calibration.json`, it must parse and contain every key the scripts read; the key list is derived from the scripts' source each time. Before Claude finishes, a changed script or `calibration.json` needs an entry in the design system's `CHANGELOG.md`, and a new copy file needs a row in the register below. The hooks need an interpreter with the pipeline's packages: `$SDR_COVER_PYTHON`, a `.venv` beside the scripts, or `~/.venvs/sdr-covers`. Tests: `python3 -m unittest discover -s .claude/hooks`.

## Register of shipped covers

| Title | Type | Trim | Pages | Spine | Ground |
|---|---|---|---|---|---|
| 1 Peter | Book Study | 6x9 | 189 | 0.4725in | Soot `#2a2a26` |
| 1 Timothy: Grace Abounding in the Dust | Book Study | 6x9 | 203 | 0.5075in | Gunmetal `#323232` |
| A 365-Day Devotional Through the Psalms (Universal Edition) | 365-Day Devotional | 6x9 | 373 | 0.9325in | Verdigris `#1b3b40` |
| A 365-Day Journey Through the Bible | 365-Day Devotional | 6x9 | 371 | 0.9275in | Slate `#26302f` |
| Benedictions, Blessings & Doxologies: From Dust to Doxology (replaces the 14-page Scriptural Catalog cover: Topical Study, 8.5x11, 14pp, blank spine, Navy `#1e2733`) | Topical Study | 8.5x11 | 176 | 0.44in | Sapphire `#15264a` |
| Colossians: The All-Sufficient Christ | Book Study | 6x9 | 201 | 0.5025in | Regal `#211b47` |
| Confession & Repentance (Part Three) | Topical Study | 8.5x11 | 127 | 0.3175in | Marrow `#211b16` |
| Dust, Breath, Fall, Promise: A Study in Genesis 1–17 | Topical Study | 8.5x11 | 168 | 0.42in | Peat `#2e2a18` |
| Dusty and Holy: A Twelve-Week Walk Through Hebrews 8–10 | Topical Study | 8.5x11 | 161 | 0.4025in | Veil `#3a1b32` |
| Dusty but Hopeful: A Twelve-Week Walk Through Romans 6–8 | Topical Study | 8.5x11 | 159 | 0.3975in | Tannin `#4a2318` |
| Ecclesiastes: Dust and Vapor | Book Study | 6x9 | 195 | 0.4875in | Umber `#3a281c` |
| Ephesians: Raised from the Dust with Christ | Book Study | 6x9 | 191 | 0.4775in | Dusk (pairing 01) `#2a4038` |
| Formed and Sent (Part Two) | Topical Study | 8.5x11 | 234 | 0.585in | Iron `#23282b` |
| Galatians: Freed from the Dust by Grace Alone | Book Study | 6x9 | 189 | 0.4725in | Bark `#2e2117` |
| In Christ: The Blessings and Benefits of Being in Christ | Topical Study | 8.5x11 | 128 | 0.32in | Clay `#3a2420` |
| James: More Grace for the Dust | Book Study | 6x9 | 202 | 0.505in | Coal `#1b1b1b` |
| John: That You May Believe — Part One | Book Study | 6x9 | 211 | 0.5275in | Blue-grey `#385569` (approx.) |
| John: That You May Believe — Part Two | Book Study | 6x9 | 215 | 0.5375in | Blue-grey `#385569` (approx.) |
| John: That You May Believe — Part Three | Book Study | 6x9 | 212 | 0.53in | Blue-grey `#385569` (approx.) |
| John: That You May Believe — Part Four | Book Study | 6x9 | 210 | 0.525in | Blue-grey `#385569` (approx.) |
| Law and Gospel: The End of Performance, the Riches of Faith | Topical Study | 8.5x11 | 165 | 0.4125in | Stone `#33383a` |
| Life (Part Four) | Topical Study | 8.5x11 | 165 | 0.4125in | Deep-pine `#1f2f2a` |
| Out of the Dust (Part One) | Topical Study | 8.5x11 | 219 | 0.5475in | Soil `#241a12` |
| Philippians: Joy from the Dust in Christ Alone | Book Study | 6x9 | 178 | 0.445in | Char `#1c1611` |
| Prayer | Topical Study | 8.5x11 | 195 | 0.4875in | Smolder `#3d1c0c` |
| Promise, Struggle, Exile, Providence: A Study in Genesis 18–50 | Topical Study | 8.5x11 | 187 | 0.4675in | Basalt `#2a2530` |
| Revive Me: A Journey Out of the Dust | Book (single-volume hardcover) | 6x9 | 234 | 0.711in (KDP hardcover; computed for 232pp, recheck for 234) | Ochre `#3e2c0e` |
| The Gospel | Topical Study | 8.5x11 | 156 | 0.39in | Garnet `#2e1013` |
| The Holy Spirit | Topical Study | 8.5x11 | 151 | 0.3775in | Deep Teal `#12302c` |
| The Sermon on the Mount: Seeing Your Sin, and the Sufficiency of Christ | Topical Study | 8.5x11 | 163 | 0.4075in | Storm `#34383e` |
| The Ten Commandments: Fulfilled and Empowered | Topical Study | 8.5x11 | 183 | 0.4575in | Cinder `#2c211e` |

The John covers' Blue-grey is the approximate colour of their rendered back panel, not a named ground from `CoverBlendMottlePairings`. Gunmetal, Coal, Sapphire, Ochre and Verdigris were added to `CoverBlendMottlePairings` as 39–43 on 2026-11-17.

Ground names follow the 2026-10-01 renames: Soot, Peat, Garnet, Smolder and Tannin were formerly "Ash", "Loam", "Oxblood", "Ember" and "Rust".

## Changelog

- **2026-10-02:** Removed the back-panel footer ("The Soul Dust Team" / "MARKETLIFE MINISTRIES · MARKETLIFEMINISTRIES.ORG") from every shipped cover, and raised `back_panel.content_pad_bottom_extra_frac_of_panel_height` from 0.085 to 0.12. Rebuilt and re-verified the shipped covers; no back-panel text falls within 1.6in of the trim's bottom edge on any title, clearing KDP/Amazon's 2.1in × 1.35in ISBN barcode-stamp zone with margin.
- **2026-10-02 (follow-up 1):** Delivered PDFs were found to have been built from a stale cached image; re-exported and checked the PDFs directly. Condensed the back-cover copy (secondary clauses only) on the six 6x9 titles with the least bottom margin: 1 Peter, Colossians, Ecclesiastes, Galatians, Philippians, and A 365-Day Journey Through the Bible.
- **2026-10-02 (follow-up 2):** Added 6x9-only spacing tightening (line-heights and gaps on the hook, paragraphs and items) on top of a second copy pass on the same six titles, bringing them into the same blank-space band as the 8.5x11 titles.
- **2026-10-02 (follow-up 3):** Rebuilt the Ephesians cover through the standard pipeline from its own content. Footer removed.
- **2026-10-10:** Four covers were built to page counts that no longer matched their interiors, so their spines were the wrong width. Rebuilt with the current count: Ephesians 225 → 191 (0.5625 → 0.4775in), The Holy Spirit 116 → 151 (0.29 → 0.3775in), Prayer 185 → 195 (0.4625 → 0.4875in), The Gospel 157 → 156 (0.3925 → 0.39in). Rule added: take the page count from the current interior PDF and recheck it before each export.
- **2026-11-17:** The October fixes had been applied in a build session's own copy of the scripts and never reached the design system, GitHub or any SDR-cover-pipeline.zip, so a new cover would have brought the footer back. Restored them here: footer removed from `gen_covers.py`; `content_pad_bottom` 0.12 in `calibration.json`; the 6x9 spacing moved into `calibration.json` as `back_panel_6x9` (it had been hardcoded). `verify_covers.py` gained a check that fails any back-panel text within 1.6in of the bottom trim, and its keyline check now looks for a whole gold line rather than the first gold pixel. `titles/1-peter.json` updated to the condensed copy as shipped. Merged this README with the design system's (adds 1 Timothy, James, John Parts 1–4, Revive Me, the Benedictions study and the Psalms devotional to the register; keeps the October corrections). Confirmed the background matches the shipped covers in Claude Code Covers and documented that it differs from the CoverBlendMottlePairings swatch recipe. Verified by rebuilding 1 Peter, Galatians, The Ten Commandments and Prayer against their shipped PDFs.
- **2026-11-18:** Turned the October lessons into hard guards that stop a bad build, in a new `guards.py` the scripts share (standard library only). `to_pdf.py` now takes one title and a required `--interior <manuscript.pdf>`, and refuses to export if the interior's page count isn't the copy file's `pages` (the 2026-10-10 spines), if the PNG is older than its HTML, copy file or `calibration.json` (the 2026-10-02 stale export), or if `verify_covers.py` hasn't stamped that exact PNG (`build/.verified-<key>`, its SHA-256). `render.py` stops if the hero photo is missing or doesn't load, instead of rendering without it, and on macOS installs the bundled fonts where Chromium can see them. `gen_covers.py` refuses a copy file with any footer field, or a ground already in the register under another title. All scripts honour `$SDR_COVER_BUILD` for a scratch build folder. Added Claude Code hooks at the repo root (see Guards and hooks). Verified by rebuilding 1 Peter and The Ten Commandments end to end against their interiors (189 and 183 pages) and shipped PDFs (mean pixel difference 4.7 and 3.5/255), and tripping each guard on a bad input. Known issue, not changed: verifying all titles in one `verify_covers.py` run fails the cross-title spine-title check on James (ink 30px against 39–41px), because the check measures rendered ink, which depends on the title's letters; its CSS size is correct.
