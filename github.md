repo: mbrown-star/study-platform-scaffold
branch: main
## Sync from Claude design system: reorganization
date: 2026-10-01
source: "Soul Dust Revival" design system in Claude (the master copy). This repo is the backup, synced at the end of each session.
- Finished cover PDFs removed. They now live in the shared drive under *Claude Code Covers*, one folder per title with its build notes. Only the Ephesians reference stays, in `assets/applied-covers/`.
- READMEs rewritten as current rules, with history in `CHANGELOG.md`.
- Ground renames: 28 Soot, 30 Garnet, 32 Smolder, 33 Peat, 36 Tannin (files renamed).
- Inferred tokens approved; `ember-700` `#b8501f` added.
- `WraparoundCover` spine series/imprint 19/22px → 56px.
- Brand marks regenerated in real Anton: SVG with outlined text, plus 2x and 4x PNGs.

## Sync from Claude design system
date: 2026-10-01
source: "Soul Dust Revival" design system in Claude (built from this repo at `828149b`, then extended there)
### Updated in this repo to match
- **Palette switched to "sunset"** in `tokens/colors.css`: ink `#1a120c`, dusk `#3a281c`, parchment `#f7ecd8`, ember `#e2762c`, gold `#f6c453`, moss `#6b5344`. `surface-sunken` and `border-default` are now literal values (were `color-mix()`). Added `surface-fill`, `text-tertiary`, `state-success`, `state-warning` (inferred, not from source; confirm) and `state-error-strong`. The previous palette is recorded at the bottom of `colors.css` and `readme.md`.
- **Display font Fraunces → Anton** (`tokens/typography.css`, `tokens/fonts.css`).
- **New assets**: `assets/brand-marks/` (3 PNGs), cover blends and mottles `16`–`38` (480px), `assets/applied-covers/` (Ephesians example, `calibration.json`, `verify_covers.py`) and `assets/wraparound-covers/` (23 finished cover PDFs + build log). The full-resolution `01`–`15` originals were kept, not replaced by Claude's 480px copies.
- **New components**: `components/covers/WraparoundCover` (promoted from code hand-written into Claude's bundle into a real source file, and added to `_ds_bundle.js`) and `components/covers/CoverBlendMottlePairings.html`.
- **Guidelines cards** retokenized. They previously referenced `--neutral-*`/`--amber-*` variables that no longer existed. Added `brand-cover` and `brand-marks` cards.
- **`readme.md` and `SKILL.md` rewritten.** They still described the system as having no brand.
- `_ds_manifest.json` tokens, cards and components updated to match.

## Earlier sync (from study-platform-scaffold)
date: 2026-07-29T14:50:37Z
### Updated in this project
- Discovered the source repo now carries a real, live brand: **Soul Dust Revival** (Psalm 119:25 theme) — tailwind tokens `ink #17231f`, `dusk #2a4038`, `parchment #f7f2e6`, `ember #de3a2e`, `gold #f0b93e`, `moss #4b6358`, fonts Fraunces/Source Serif 4/Archivo.
- Replaced the placeholder neutral/amber palette in `tokens/colors.css` and system-font stack in `tokens/typography.css` with these real values; added `tokens/fonts.css` (`@font-face` for Fraunces, Source Serif 4, Archivo).
- Rebuilt `Soul Dust Revival Homepage.html` to match the real `DustHero`/`SiteHeader`/`SiteFooter` components (gold→ember→ink gradient hero with rising dust motes, "Start where you are" product grid, "How a study works" 3-step section, "From the blog" section) instead of the earlier invented sunset-photo hero.
- Confirmed public pages `/`, `/books`, `/books/[slug]`, `/blog`, `/blog/[slug]` are real dynamic pages reading `products`/`posts`, and roles (`admin`/`leader`/`user`), leader resources, and social scheduling exist in source but aren't yet reflected in the UI kits here.

## Screen map
| Screen | Repo source |
|---|---|
| Homepage hero | `components/marketing/DustHero.tsx`, `app/globals.css` (`.dust-mote`/`@keyframes dust-rise`) |
| Site header/footer | `components/marketing/SiteHeader.tsx`, `components/marketing/SiteFooter.tsx`, `components/marketing/CartLink.tsx` |
| Homepage sections | `app/(marketing)/page.tsx` |
| Books catalog | `app/(marketing)/books/page.tsx` |
| Blog index | `app/(marketing)/blog/page.tsx` |
| Login/signup | `components/auth/AuthForm.tsx` |
| Storefront/checkout UI kit | `app/(marketing)/checkout/*`, `components/commerce/AddToCartButton.tsx` (not yet re-styled to real brand — next sync) |
| Admin UI kit | `components/admin/*` (not yet re-styled to real brand — next sync) |
