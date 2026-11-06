# Changelog

Newest first. Dates before 2026-10-01 are approximate, reconstructed from the old READMEs. Each entry says what changed and why. The current rules are in the README and each group's README. Detailed per-title build notes for finished covers are in the shared drive under *Claude Code Covers → <title> → Build notes*.

## 2026-11-05 (overnight): web-app currency audit, two new components, stale compositions flagged
- **Why:** asked to bring the whole system current for the web app and web app alone — not just covers — since the live `soul-dust-revival` site had drifted far ahead of what this system documented, while only the color tokens had actually been kept in sync (the 2026-11-05 parchment/gold-700 entries below). The three page compositions (`Storefront`, `StudyApp`, `AdminConsole`) turned out to still be exactly what was compiled from the *original, pre-customization* scaffold on 2026-09-21 — none of the real site's subsequent changes (documented at length in the site's own `CLAUDE.md`) had ever reached them.
- **README.md:** fixed the Visual Foundations color section, which still quoted the retired `#f7ecd8` parchment and never mentioned `gold-700` or `error`/`state-success`/`state-warning` — now matches `tokens.json` exactly (tokens.json itself was already current; only the prose had drifted). Added a dated "Web app — current state" section as the honest, current source of truth: shared-shell nav structure, the new `format: "both"` commerce model, admin delete, the Tiptap rich-text unification, and an explicit list of what this audit did *not* reach (checkout/cart line items, account/login/order-confirmation pages, blog/leader-resources at their current width, admin Users/Reports/Social). Reordered the opening paragraph to name the web app as the actively-developed product, with covers framed as the (large, but one-at-a-time) secondary system.
- **Two new components, built from the live site's real source, not the old scaffold:**
  - `PurchaseOptions` (new `Commerce` group) — the format `"both"` dual physical/digital purchase panel from `app/(marketing)/books/[slug]/page.tsx`.
  - `AdminFormActions` (added to `Forms`) — the Save/Delete button pair from `ProductForm`/`BlogPostForm`/`StudyForm`, including an explicitly flagged gap: the live buttons currently use Tailwind's stock `neutral-900`/`red-600`, not this system's `ink`/`error` tokens. Documented as a live-code fix still needed, not quietly matched.
- **`Storefront`, `StudyApp`, `AdminConsole` READMEs** each got a dated "stale as of 2026-11-05" note naming the specific real changes that happened underneath them, so a reader isn't misled into thinking these click-throughs are current.
- **Not done:** an actual rebuild of those three compositions from the live codebase (a proper `from-code.md`/`/design-sync`-style pass) — that's a larger job than an overnight audit, and is now explicit in Open items so it doesn't get lost.

## 2026-11-05: parchment lightened; PaletteOptions component added
- `parchment` changed from `#f7ecd8` (visibly cream/tan) to `#fefdfa` (near-white, a bare hint of warmth), per a nav-bar color review. Every token whose usage note quotes a contrast figure "on parchment" was recomputed against the new value (all improved, since the new background is lighter): `ink` 15.8→18.2:1, `dusk` (as a text-on-ink-surface figure) 11.96→13.76:1, `ember` 2.62→3.01:1, `ember-700` 4.27→4.91:1 (now clears AA for body text on parchment itself, though the large-text-only guidance stays for darker light-surfaces like `surface-sunken`), `gold` 1.39→1.60:1, `gold-700`/`state-warning` 4.53→5.22:1, `moss` 6.09→7.01:1, `text-tertiary` 4.87→5.60:1, `state-error` 5.78→6.65:1, `state-success` 6.69→7.70:1. `surface-sunken` (a documented 92% paper / 8% dusk blend) recomputed to `#eeebe8`.
- `dusk` itself was reviewed against three alternatives — a cool slate-grey "true dusk," a muted indigo-violet twilight, and a desaturated warm-charcoal compromise — for the nav bar specifically, but kept as-is (`#3a281c`); none of the alternatives were adopted.
- Added `PaletteOptions`, a Foundations component recording this review (all four `dusk` options and four `parchment` options, each shown in context — a page-background demo for parchment, the live nav-bar monogram+wordmark treatment for dusk — with the adopted ones marked), alongside the existing `Palette` component.

## 2026-11-05: gold-700 token
- Added `gold-700` `#8d6407`, mirroring `ember-700`: gold itself is 1.39:1 on parchment (fills and large display type only), so small gold-family accent text/links on parchment now has an AA-passing option at 4.53:1, instead of either failing contrast or borrowing `state-warning`'s value for non-warning text.

## 2026-10-19: Benedictions, Blessings & Doxologies study cover
- Benedictions, Blessings & Doxologies cover added: Topical Study, 8.5x11, 176pp, ground Sapphire `#15264A` (new, from the Revelation 5 throne scene), spine 0.44in. Copy file `titles/benedictions-study.json`. It replaces the earlier 14-page Scriptural Catalog cover (Navy `#1E2733`, blank spine) for the same title, whose register row is superseded.
- Rebuilds from the copy file and passes `verify_covers.py` (16/16). The shipped PDF was built outside this repo's checks, so a rebuild may differ from it; no pixel comparison was made.

## 2026-10-12: John covers added, Revive Me page count corrected
- John: That You May Believe, Parts One to Four added: Book Study, 6x9, ground Blue-grey `#385569` (approximate, read off the rendered back panel; not a named ground), 211 / 215 / 212 / 210pp, spines 0.5275 / 0.5375 / 0.53 / 0.525in. Copy files `titles/john-part-1.json` to `john-part-4.json`, transcribed from the delivered covers (no text layer) and confirmed by Matt. They rebuild and pass `verify_covers.py` (69/69), but the shipped PDFs were built outside this pipeline, so a rebuild may differ from them.
- Revive Me page count corrected from 232 to 234, per its interior PDF. The 0.711in spine and 14.2867in x 10.4167in wrap still match the 232-page calculation, so they need rechecking against KDP's hardcover calculator for 234pp before upload.

## 2026-10-10: Revive Me cover
- Revive Me cover added: single-volume hardcover, 6x9, 234pp (corrected 2026-10-12; originally logged as 232), ground Ochre `#3e2c0e`. Spine 0.711in and board/wrap/hinge geometry come from KDP's hardcover calculator, not the pages x 0.0025in paperback formula.
- No copy file: it was built without the pipeline zip (from the John covers as references), so it can't be rebuilt from `titles/` yet. A hardcover mode in `gen_covers.py` is still to do.

## 2026-10-06: 1 Timothy and James covers
- 1 Timothy cover added: Book Study, 6x9, 203pp, ground Gunmetal `#323232`. Copy file `titles/1-timothy.json`.
- James cover added: Book Study, 6x9, 202pp, ground Coal `#1b1b1b`. Copy file `titles/james.json`.
- Both rebuild from the copy files and pass `verify_covers.py` (16/16). Their Drive build notes say they were built with a locally patched pipeline (2026-10-02 directives: no back-panel footer, bottom pad 0.12, `six_by_nine_back_tightening` in `calibration.json`) that isn't saved here yet, so a rebuild from this folder may differ slightly from the shipped PDFs.

## 2026-10-01: cover requests ask for both inputs
- Every cover request now starts by confirming the study's manuscript PDF and `SDR-cover-pipeline.zip` are in hand, asking for whichever is missing.
- The pipeline bundles its own fonts (Liberation Serif, DejaVu Serif Condensed) so it renders identically in a Claude Chat sandbox.

## 2026-10-01: cover pipeline rebuilt
- `gen_covers.py`, `render.py` and `to_pdf.py` rebuilt from the cover rules (the originals were never saved), and `verify_covers.py` generalized to every title. Proven by rebuilding The Ten Commandments (8.5x11) and 1 Peter (6x9): mean pixel difference about 4.5/255 against the shipped PDFs, text within 0-3px, identical page sizes; verify passes 37/37.
- `calibration.json` gained `fixed_px_at_300dpi`: the back panel and the front's secondary lines are fixed pixel sizes on every trim, measured off the shipped covers. Spine sizes corrected to what the shipped covers actually use: DejaVu Serif Condensed, series 56px, title 54px, imprint 54px (the earlier 62px was an ink measurement). `WraparoundCover` updated to match.
- Copy files for both titles are in `assets/applied-covers/titles/`.

## 2026-10-01: article text and heading case
- Anton titles stay uppercase, but headings inside long-form articles (lessons, blog, leader resources) now use normal case.
- Article text uses brand colors: ink body, headings, links and quotes, moss secondary text, ember link underlines and quote borders. Previously the web app used Tailwind's default grey.

## 2026-10-01: ink focus ring
- `focus-ring` changed from gold to ink: gold is only 1.39:1 on parchment, below the 3:1 minimum for focus indicators. Added `focus-ring-on-dark` (gold) for ink and dusk sections. Components that use `focus-ring` pick this up automatically.

## 2026-10-01: error color and web app port
- `state-error` changed from ember (2.62:1, fails as text) to `#a8301c` (5.78:1 on parchment), so error messages pass WCAG AA.
- The study-platform-scaffold web app now takes its colors and fonts from these tokens (CSS variables in `app/globals.css`, mapped in `tailwind.config.js`, Anton via `next/font`).

## 2026-10-01: reorganization
- Finished cover PDFs moved to the shared drive (*Claude Code Covers*, one folder per title with its build notes). Only the Ephesians reference stays here, in `applied-covers`. Duplicate files outside `project/` removed.
- READMEs rewritten as current rules. Their build history moved into this changelog.
- Components regrouped: Foundations, Forms, Feedback, Navigation, Data display, Covers, Pages, Archive (old homepage drafts). The Components tab doesn't show group headings, so the README carries a by-group table, the live components are listed in group order, and divider rows (Forms, Feedback, Navigation, DataDisplay, Covers) head each group.
- Production grounds renamed so every name is unique: 28 Ash → **Soot**, 33 Loam → **Peat**, 30 Oxblood → **Garnet**, 32 Ember → **Smolder**, 36 Rust → **Tannin**. Hex values and images unchanged. Files renamed to match.
- The four inferred tokens (`surface-fill`, `text-tertiary`, `state-success`, `state-warning`) approved as-is.
- Added `ember-700` `#b8501f` for small accent text, since ember and gold are too light for text on parchment.
- `WraparoundCover` spine series-name and imprint sizes 19/22px → 56px, matching `calibration.json` and the printed covers.
- Brand marks regenerated with the real Anton face (they previously used a stand-in font). Added SVGs with outlined text, plus 2x and 4x PNGs. The lockup's two wordmark lines got 3px of space between them because they touched in real Anton, and the "Psalm 119:25" line is now set in Source Serif 4 italic (it was a Georgia fallback).
- GitHub repo synced to this system. From now on it's the backup and is synced at the end of each session.

## 2026-10-01: The Ten Commandments cover
- Topical Study, 8.5x11, 183pp, ground Cinder. Built straight from `calibration.json`, clean on the first render.

## 2026-09-28 to 2026-09-30: series covers
- Built 1 Peter, Benedictions, The Gospel, The Holy Spirit, Prayer, Genesis Parts 1 and 2, Dusty and Holy, Dusty but Hopeful, Colossians, The Sermon on the Mount, the 365-Day Journey, Ecclesiastes, Galatians, In Christ, Law and Gospel and Philippians. Lessons that became rules:
  - Long titles (Benedictions, 365-Day Journey) use the manuscript's own two-line break, and the 365-Day spine carries only the title's first line.
  - Spines under 79 pages stay blank (Benedictions, 14pp).
  - A bounded range within a book is a Topical Study at 8.5x11 even if the book appears on the Book Study list (Dusty but Hopeful, Romans 6–8).
  - Back-panel overflow from a long hook (Colossians, Ecclesiastes) or from cumulative copy length (Philippians): keep the hook to one sentence under ~75 characters.
  - A long subtitle wrapped the tagline into the fixed rule (Law and Gospel), so taglines must stay on one line.
- **Design directive (2026-09-28):** the spine's series name and imprint line render 56px (title 62px minus 6px) on every title. `calibration.json` was updated. Ephesians' already-printed cover was not rebuilt.

## 2026-09-22 to 2026-09-27: four-part study and the calibration pipeline
- Built *Out of the Dust*, *Formed and Sent*, *Confession & Repentance* and *Life* from scratch to match Ephesians. It took nine layout passes. The fixes that stuck: medium-weight one-line title sized by character count; cream series name; separate height/width keyline insets; each spine line as its own vertical-writing element; spine type in fixed 300dpi pixels, never scaled by spine width (scaling by each title's own width made the four look inconsistent, and scaling to the narrowest made them all too small).
- Introduced `calibration.json` (the single source of every layout number, measured from the Ephesians print PDF at 300dpi) and `verify_covers.py` (a rendered-pixel check that must pass before delivery).
- Added "A Journey" / "A Journey Part [N]" to the four-part study only.

## 2026-09-21 to 2026-09-22: cover grounds and spine blend
- Applied pairing 01 (Dusk) to the Ephesians cover at its real trim and spine. The spine went from a hard seam, to a feather that spilled into the back panel, to a smoothstep fade confined to the spine. That fade is now the standard for every wraparound.
- Extended the grounds: `16`–`27` darker variations (soil … slate), built from a recipe reverse-engineered from the originals (≈7/255 mean difference from `01`), then `28`–`38` with the production hex values from shipped covers.

## 2026-09-21: design system created
- Built from `mbrown-star/soul-dust-revival-design-system@828149b`. The sunset palette (ink `#1a120c`, ember `#e2762c`, gold `#f6c453`, Anton display) was made canonical, replacing the earlier `tokens/colors.css` palette (ink `#17231f`, ember `#de3a2e`, gold `#f0b93e`, Fraunces).
- The 12 small components render live from the repo's bundle. Storefront, StudyApp and AdminConsole were compiled from the repo's `ui_kits` JSX. The homepage, logo, palette and cover-library HTML files were added as pages.
