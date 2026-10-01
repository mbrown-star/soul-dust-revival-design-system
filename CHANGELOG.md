# Changelog

Newest first. Dates before 2026-10-01 are approximate, reconstructed from the old READMEs. Each entry says what changed and why. The current rules are in the README and each group's README. Detailed per-title build notes for finished covers are in the shared drive under *Claude Code Covers → <title> → Build notes*.

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
