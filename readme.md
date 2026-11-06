# Soul Dust Revival Design System

The design system for **Soul Dust Revival**, a Psalm 119:25 devotional ministry (*"My soul cleaves to the dust; revive me according to Your word"* — NASB). It covers the **web platform** (public storefront, gated study app, blog, leader resources and the admin console — the primary, actively-developed product, built on `mbrown-star/study-platform-scaffold`) **and** the printed book-cover system for the Book Study, Topical Study and 365-Day Devotional titles. Covers get a lot of this system's file volume (dozens of ground images, a full calibration pipeline) because they're produced one at a time by hand; the web app's tokens and live components are the part that actually ships continuously and should be read first for anything touching the site.

## How we work

- **The Soul Dust Revival design system in Claude is the master copy.** This repo is its versioned backup. Don't edit it independently: change the system in Claude, then at the end of that session copy the changes here and add a line to `github.md`.
- **Keep the web app in step — both directions.** `mbrown-star/study-platform-scaffold` (built out as the real `soul-dust-revival` project) takes its colors from CSS variables in `app/globals.css` (mapped in `tailwind.config.js`) and its fonts from `app/layout.tsx`. When a color or font changes here, update those files in the same session — and the reverse: when the live site's own build adds or changes a token, a component, or a real page/flow, that needs to land here too, not just in the site's own `CLAUDE.md`. **This system had drifted on the second direction** — see "Web app — current state" below for what that audit found and what it didn't reach.
- **Log every change** as a dated entry at the top of the Changelog section (`CHANGELOG.md`): what changed and why, in a few lines. This README holds only the current rules. History goes in the changelog.
- **Finished covers don't live here.** Each print-ready cover PDF goes in the shared drive under *Soul Dust Revival → [Claude Code Covers](https://drive.google.com/drive/folders/17VHHakHBc2b0LlbSSa_JYw1e3bshOl4M) → <title>*, with that title's build notes. This system keeps only what's needed to *make* a cover (see Covers below).
- **Starting a cover:** Before starting any cover, make sure you have both: the study's manuscript PDF (ask for it if it wasn't provided) and `SDR-cover-pipeline.zip`, the cover scripts, fonts and hero photo (ask for it if it isn't already in the conversation). Don't start without both.
- **Building a cover:** read the rules in `assets/applied-covers/README.md` → pick an unused ground from `CoverBlendMottlePairings` → write `titles/<key>.json` → `gen_covers.py` (reads every number from `calibration.json`) → `render.py` → `verify_covers.py` must exit 0 → check the full, back, front and spine crops → export the PDF to the Covers folder → add the title to the register and the changelog.
- **Undecided things stay out of the rules.** Open questions go in the "Open items" section below until they're decided.

## Content fundamentals

- **Direct and functional, never marketing-voiced.** Buttons say exactly what happens: "Proceed to payment," "Send login link," "Save product," "Delete product," "Import document." Never "Get started" or "Let's go."
- **"You/your" for the reader, plain first person only in confirmations.** "Check your email for a login link." / "Thank you for your order."
- **Sentence case** in the app. ALL CAPS only for the small tracked block-type labels ("TEXT", "CALLOUT") and Anton titles.
- **No exclamation points, no emoji, no hype.** Errors are specific and calm: "This product has order history and can't be deleted. Mark it inactive instead."
- **Devotional labels are short and plain:** "Key Verse," "Reflection," "Prayer Prompt."

## Visual foundations

- **Color: the sunset palette.** Ink `#1a120c` on parchment `#fefdfa` (lightened 2026-11-05 from the original cream `#f7ecd8` — see `PaletteOptions`). Dusk `#3a281c` for deep sections and footers, moss `#6b5344` for secondary text. **Ember `#e2762c`** is the one chromatic accent and **gold `#f6c453`** the highlight.
- **Contrast rule:** ember (3.01:1 on the current parchment) and gold (1.60:1) never carry small text on parchment. Use them for buttons, fills and large display type. For small accent text (links, inline emphasis) use **`ember-700` `#b8501f`** (4.91:1) or **`gold-700` `#8d6407`** (5.22:1); use ink or moss for ordinary body copy. `error` `#a8301c`, `state-success` `#3b5a2b` and `state-warning` (= `gold-700`) are the three status colors, each AA-passing at any size on parchment.
- **Type:** **Anton** for display (headlines, hero, wordmark) at its native weight 400, often gradient-clipped ember→gold. Page and section titles are uppercase with leading ~0.92. Headings *inside* long-form articles (lessons, blog, leader resources) stay in normal case so long headings read easily. **Source Serif 4** for reading (lessons, blog). **Archivo** for UI (buttons, labels, nav, forms), with semibold headings. All three load from Google Fonts.
- **Article text** (lessons, blog, leader resources): body, headings, links and quotes in ink; lead text, list markers and captions in moss; links underlined in ember; quote borders ember. These pages use the site's standard `max-w-5xl mx-auto px-4` content width (see "Web app — current state"), with the prose column itself capped narrower for readability.
- **Spacing:** 4px-based scale. Columns are narrow and centered: 24rem login, 32rem admin forms, 36rem checkout, 42rem lesson reading. The admin shell's own content column was widened from 56rem (`max-w-4xl`) to the site's full standard 80rem (`max-w-5xl`) on 2026-11-05 — it's no longer a narrower exception; see below.
- **Borders over shadows:** 1px `border-default` and 8px corners on cards, fields, dividers and buttons. The only shadow is `shadow-popover`, on the admin's one popover menu.
- **Focus:** every interactive element gets a 2px outline with a 2px offset (WCAG 2.4.7). Use `focus-ring` (ink) on light grounds (15.8:1+ on parchment) and `focus-ring-on-dark` (gold) on ink and dusk sections. Never use gold on parchment, where it's only 1.60:1. Never remove the ring.
- **Motion:** functional only (progress-bar fill, hover/focus transitions) and always honors `prefers-reduced-motion`. The hero's rising dust motes are the one decorative motion. A `.mottle` cloud-blotch/grain/vignette texture (ported from the cover system's own mottle treatment, see `CoverMottleLibrary`) is applied to the homepage's dusk band and the site footer as of 2026-11-05 — the one place cover texture and web-app surface share a treatment; not applied elsewhere.
- **App backgrounds** are flat parchment or a light fill, except the one `.mottle` application above. Gradients, photography and texture otherwise belong to the marketing hero and the book covers.

## Iconography

No icon set. The few icons are Unicode glyphs in text: `⠿` drag handle, `↑`/`↓` reorder, `✓` success, `+` add, and a text "Remove"/"Delete" link. No emoji. If an icon set is ever needed, Lucide is the closest match.

## Brand marks

`assets/brand-marks/`: the stacked wordmark (primary), the monogram + wordmark lockup (used in the site's shared nav-bar shell — see below — and footers) and the SDR monogram badge (favicons, avatars). Each comes as an SVG (text converted to outlines, safe for print at any size), a PNG at 2x and a PNG at 4x. See `LogoVariations` for all five lockup options.

## Web app — current state

The web app is the actively-developed product and changes far more often than this system has been kept current with. This section is the honest status as of **2026-11-05**, written from the live site's own source and its `CLAUDE.md` build log, not from the (now stale) `AdminConsole`/`Storefront`/`StudyApp` page compositions below, which were compiled once from the original scaffold's pre-customization `ui_kits/*.jsx` on 2026-09-21 and have not been resynced since. Read this section for what's actually true today; treat those three compositions as historical reference only until they're rebuilt from the live site (see each one's own README for what specifically has since changed under it).

**Navigation.** Every top-level nav bar — public and admin — renders through one shared shell (`SiteHeaderShell`: sticky, `bg-ink/95` with backdrop blur, the monogram+wordmark lockup on the left, routing home) so the two can't drift apart in size or color. The public nav (`SiteNav`) groups public links first (Books & Studies, Blog, Cart, "Log in" when signed out), then a divider, then logged-in-only items (Your Studies, a "Profile" dropdown with Account/Admin-when-admin/Log out). The admin nav (`AdminNav`) sits in the same shell and no longer has its own narrower content column — see Spacing above. Nav links and the logo use a text-color-only focus indicator (color shift, no box) rather than a ring, by explicit decision, scoped to just these two nav bars.

**Commerce / products.** A product's `format` is `physical`, `digital`, or (added 2026-11-05) **`both`** — sold as two fully independent purchases, each with its own price and own Stripe Price, not a combined bundle. See the new `PurchaseOptions` component for the detail-page treatment and the admin's two-fieldset form (also new); a cart line and a checkout/order line both carry which variant (`physical`/`digital`) they are. A product's alt text is encouraged in the admin UI but, as of 2026-11-05, no longer enforced at all (widened from an earlier book-cover-only exemption) — a real, accepted accessibility trade-off, not an oversight.

**Admin delete.** Products, blog posts and studies (added 2026-11-05) can each be deleted from their edit form — see the new `AdminFormActions` component, including the one open compliance gap it documents (the live buttons currently use Tailwind's stock `neutral-900`/`red-600`, not this system's `ink`/`error` tokens).

**Rich text.** Blog post bodies moved from markdown to the same Tiptap-HTML editor already used for leader resources and lesson content blocks (`RichTextEditor`) — one authoring experience across all long-form admin content now, not two.

**Not yet audited into this system** (known gaps, not silently assumed fine): the checkout/cart page's line-item treatment for a "both"-format purchase; the account, login/signup, and order-confirmation pages as they exist today; the blog listing/post and leader-resources pages at their current `max-w-5xl` width; the admin Users/Reports/Social-scheduling screens; and the full current `AdminConsole` composition (products list/form, studies list/lesson editor) — all real, shipped parts of the site that this system either never had a live component for, or had one that's now stale per the compile-date note above.

## Components

Under `components/`, each as `<Name>.jsx` + `<Name>.d.ts` + `<Name>.prompt.md`, plus a preview card per folder. `_ds_bundle.js` is the pre-built bundle (namespace `StudyPlatformDesignSystem_d2afba`).

- **Forms:** Button, Checkbox, ColorPicker, Input, Textarea, Select (plus the `AdminFormActions` composition, documented in the Claude system only)
- **Feedback:** Callout, ProgressBar, StatusMessage
- **Navigation:** Tabs
- **Data display:** Badge, ProductRow
- **Commerce:** `PurchaseOptions` (format `"both"` dual-purchase panel; documented in the Claude system only, no repo component)
- **Foundations:** `PaletteOptions` (record of the 2026-11-05 color review; Claude system only)
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
- **Recipe and tooling:** `assets/applied-covers/` holds the rules, `calibration.json`, the build pipeline (`gen_covers.py`, `render.py`, `verify_covers.py`, `to_pdf.py`), one copy file per title in `titles/`, and the Ephesians reference cover.
- **Register:** every shipped title with its trim, spine and ground, so each new title can get its own ground. See `assets/applied-covers/README.md`.

## Open items

- **`surface-sunken` and `border-default`** are literal approximations of what were `color-mix()` blends in the original CSS.
- **`AdminConsole`/`Storefront`/`StudyApp` need a real resync from the live `soul-dust-revival` codebase**, not the original scaffold — a proper `/design-sync`-style pass (see this artifact type's `from-code.md`) rather than the hand-audited honesty pass this entry represents. Until then, treat "Web app — current state" above as the source of truth for anything these three compositions don't agree with.
- **The admin forms' `neutral-900`/`red-600` vs. `ink`/`error` gap** (see `AdminFormActions`) is a live-code fix, not a design-system one — flagged here so it doesn't get silently "documented around."

## Index

- `styles.css`: global stylesheet entry point (import this)
- `tokens/`: `colors.css`, `fonts.css`, `typography.css`, `spacing.css`, `borders.css`
- `guidelines/`: foundation specimen cards
- `components/`: primitives and cover components; `_ds_bundle.js` is the built bundle and `_ds_manifest.json` its manifest
- `ui_kits/`, `templates/`: product recreations
- `assets/`: brand marks, hero and cover imagery, the cover recipe and build pipeline (`applied-covers/`)
- `CHANGELOG.md`: change history (mirrors the Claude system's)
- `github.md`: sync log
- `SKILL.md`: portable skill file for use in Claude Code or elsewhere
