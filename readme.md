# Soul Dust Revival Design System

The design system for **Soul Dust Revival**, a Psalm 119:25 devotional ministry (*"My soul clings to the dust; revive me according to Your word"*). It covers the web platform (storefront, gated study app and admin console, from `mbrown-star/study-platform-scaffold`) and the printed book-cover system for the Book Study, Topical Study and 365-Day Devotional titles.

## How we work

- **The Soul Dust Revival design system in Claude is the master copy.** This repo is its versioned backup. Don't edit it independently: change the system in Claude, then at the end of that session copy the changes here and add a line to `github.md`.
- **Keep the web app in step.** `mbrown-star/study-platform-scaffold` takes its colors from CSS variables in `app/globals.css` (mapped in `tailwind.config.js`) and its fonts from `app/layout.tsx`. When a color or font changes, update those files in the same session.
- **Log every change** as a dated entry at the top of the Changelog section (`CHANGELOG.md`): what changed and why, in a few lines. This README holds only the current rules. History goes in the changelog.
- **Finished covers don't live here.** Each print-ready cover PDF goes in the shared drive under *Soul Dust Revival → [Claude Code Covers](https://drive.google.com/drive/folders/17VHHakHBc2b0LlbSSa_JYw1e3bshOl4M) → <title>*, with that title's build notes. This system keeps only what's needed to *make* a cover (see Covers below).
- **Building a cover:** read the rules in `assets/applied-covers/README.md` → take the layout numbers from `calibration.json` (never retype them) → pick an unused ground from `CoverBlendMottlePairings` and record it in the register → render → `verify_covers.py` must exit 0 → check the full, back, front and spine crops → export the PDF to the Covers folder → add the title to the register and the changelog.
- **Undecided things stay out of the rules.** Open questions go in the "Open items" section below until they're decided.

## Content fundamentals

- **Direct and functional, never marketing-voiced.** Buttons say exactly what happens: "Proceed to payment," "Send login link," "Save product," "Import document." Never "Get started" or "Let's go."
- **"You/your" for the reader, plain first person only in confirmations.** "Check your email for a login link." / "Thank you for your order."
- **Sentence case** in the app. ALL CAPS only for the small tracked block-type labels ("TEXT", "CALLOUT") and Anton display type.
- **No exclamation points, no emoji, no hype.** Errors are specific and calm: "Alt text is required whenever an image is attached (WCAG 1.1.1)."
- **Devotional labels are short and plain:** "Key Verse," "Reflection," "Prayer Prompt."

## Visual foundations

- **Color: the sunset palette.** Ink `#1a120c` on parchment `#f7ecd8`. Dusk `#3a281c` for deep sections and footers, moss `#6b5344` for secondary text. **Ember `#e2762c`** is the one chromatic accent and **gold `#f6c453`** the focus ring and highlight.
- **Contrast rule:** ember (2.62:1) and gold (1.39:1) never carry small text on parchment. Use them for buttons, fills, focus rings and large display type. For small accent text (links, inline emphasis) use **`ember-700` `#b8501f`** (4.27:1, so large text only: 18px+, or 14px+ bold), and use ink or moss for body copy.
- **Type:** **Anton** for display (headlines, hero, wordmark): uppercase, leading ~0.92, native weight 400, often gradient-clipped ember→gold. **Source Serif 4** for reading (lessons, blog). **Archivo** for UI (buttons, labels, nav, forms), with semibold headings. All three load from Google Fonts.
- **Spacing:** 4px-based scale. Columns are narrow and centered: 24rem login, 32rem admin forms, 36rem checkout, 42rem lesson reading, 56rem admin shell.
- **Borders over shadows:** 1px `border-default` and 8px corners on cards, fields, dividers and buttons. The only shadow is `shadow-popover`, on the admin's one popover menu.
- **Focus:** every interactive element gets a 2px gold outline with a 2px offset (WCAG 2.4.7). Never remove it.
- **Motion:** functional only (progress-bar fill, hover/focus transitions) and always honors `prefers-reduced-motion`. The hero's rising dust motes are the one decorative motion.
- **App backgrounds** are flat parchment or a light fill. Gradients, photography and texture belong to the marketing hero and the book covers.

## Iconography

No icon set. The few icons are Unicode glyphs in text: `⠿` drag handle, `↑`/`↓` reorder, `✓` success, `+` add, and a text "Remove" link. No emoji. If an icon set is ever needed, Lucide is the closest match.

## Brand marks

`assets/brand-marks/`: the stacked wordmark (primary), the monogram + wordmark lockup (nav bars, footers) and the SDR monogram badge (favicons, avatars). Each comes as an SVG (text converted to outlines, safe for print at any size), a PNG at 2x and a PNG at 4x. See `Soul Dust Revival Logo.html` for all five lockup options.

## Components

Under `components/`, each as `<Name>.jsx` + `<Name>.d.ts` + `<Name>.prompt.md`, plus a preview card per folder. `_ds_bundle.js` is the pre-built bundle (namespace `StudyPlatformDesignSystem_d2afba`).

- **Forms:** Button, Checkbox, ColorPicker, Input, Textarea, Select
- **Feedback:** Callout, ProgressBar, StatusMessage
- **Navigation:** Tabs
- **Data display:** Badge, ProductRow
- **Covers** (`components/covers/`): `WraparoundCover` (live, prop-driven preview of the calibrated cover layout) and `CoverBlendMottlePairings.html` (all darker grounds beside their mottles)

`Button` variants `secondary`/`ghost`/`danger` and the named `Badge`/`StatusMessage` are intentional additions beyond the app source. Callout backgrounds are free-form per instance (`#fef3c7` by default, any hex allowed) and are not tied to the tokens.

## Pages and reference sheets

The top-level HTML files are the brand's source documents. In the Claude system they're grouped as:

- **Foundations:** `Soul Dust Revival Palette.html`, `Soul Dust Revival Logo.html`
- **Covers:** `Blended Cover Grounds.html`, `Book Cover Library - Mottled Colors.html`, `Book Cover Library - Image Treatments.html`, `Hero Image Variations.html`
- **Pages:** `Soul Dust Revival Homepage.html` (current), plus `ui_kits/storefront`, `ui_kits/study-app` and `ui_kits/admin` (also as `templates/`)
- **Archive:** `Soul Dust Revival Homepage v2.html`, `v3.html` and `Homepage Variations.html` (earlier drafts)

## Covers

- **Grounds:** `assets/cover-mottles/` (flat color + mottle texture) and `assets/cover-blends/` (the hero photo, duotoned and blended onto that mottle), 38 of each, numbered in pairs. Every ground has one unique name. `components/covers/CoverBlendMottlePairings.README.md` lists every name and hex value. `01`–`15` and the hero variants are full resolution here; `16`–`38` exist only at 480px.
- **Recipe and tooling:** `assets/applied-covers/` holds the rules, `calibration.json`, `verify_covers.py` and the Ephesians reference cover.
- **Register:** every shipped title with its trim, spine and ground, so each new title can get its own ground. See `assets/applied-covers/README.md`.

## Open items

- **`gen_covers.py`, `render.py` and `to_pdf.py` aren't stored anywhere.** They lived in earlier build sessions. Until they're saved alongside `calibration.json`, every cover rebuild depends on recreating them.
- **`surface-sunken` and `border-default`** are literal approximations of what were `color-mix()` blends in the original CSS.

## Index

- `styles.css`: global stylesheet entry point (import this)
- `tokens/`: `colors.css`, `fonts.css`, `typography.css`, `spacing.css`, `borders.css`
- `guidelines/`: foundation specimen cards
- `components/`: primitives and cover components; `_ds_bundle.js` is the built bundle and `_ds_manifest.json` its manifest
- `ui_kits/`, `templates/`: product recreations
- `assets/`: brand marks, hero and cover imagery, cover recipe and tooling (`applied-covers/`)
- `CHANGELOG.md`: change history (mirrors the Claude system's)
- `github.md`: sync log
- `SKILL.md`: portable skill file for use in Claude Code or elsewhere
